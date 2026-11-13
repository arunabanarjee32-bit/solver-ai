import { z } from "zod";

const problemSummarySchema = z.object({
  id: z.string().min(1).max(100),
  slug: z
    .string()
    .min(1)
    .max(100)
    .regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/),
  title: z.string().min(1).max(200),
  difficulty: z.enum(["Easy", "Medium"]),
  tags: z.array(z.string().min(1).max(80)).max(20),
  summary: z.string().min(1).max(2_000),
  estimated_minutes: z.number().int().min(1).max(1_440),
});

const problemSchema = problemSummarySchema.extend({
  statement: z.string().min(1).max(50_000),
  input_format: z.string().min(1).max(10_000),
  output_format: z.string().min(1).max(10_000),
  constraints: z.array(z.string().min(1).max(2_000)).min(1).max(100),
  samples: z
    .array(
      z.object({
        input: z.string().max(50_000),
        output: z.string().max(50_000),
        explanation: z.string().max(10_000),
      }),
    )
    .min(1)
    .max(20),
  starter_code: z.object({
    python: z.string().max(100_000),
    cpp: z.string().max(100_000),
  }),
  hints: z.array(z.string().min(1).max(10_000)).max(20),
  provenance: z.object({
    author: z.string().min(1).max(200),
    source: z.string().min(1).max(2_000),
  }),
});

const problemPageSchema = z
  .object({
    items: z.array(problemSummarySchema).max(100),
    total: z.number().int().nonnegative(),
    limit: z.number().int().min(1).max(100),
    offset: z.number().int().min(0).max(10_000),
  })
  .refine(
    (page) =>
      page.items.length <= page.limit &&
      (page.items.length === 0 ||
        page.total >= page.offset + page.items.length),
  );

export type ProblemSummary = z.infer<typeof problemSummarySchema>;
export type Problem = z.infer<typeof problemSchema>;
export type ProblemPage = z.infer<typeof problemPageSchema>;

export const PRACTICE_REQUEST_TIMEOUT_MS = 10_000;

class PracticeServiceError extends Error {}

function responseSchema(path: string) {
  const pathname = path.split(/[?#]/, 1)[0];
  if (pathname === "/api/v1/problems") return problemPageSchema;
  if (/^\/api\/v1\/problems\/[^/]+$/.test(pathname)) return problemSchema;
  // New endpoints must opt into a schema instead of silently trusting a cast.
  throw new PracticeServiceError("This practice request is not supported.");
}

function invalidResponse() {
  return new PracticeServiceError(
    "The practice service returned an invalid response. Please try again.",
  );
}

export async function getJSON<T>(
  path: string,
  signal?: AbortSignal,
): Promise<T> {
  const schema = responseSchema(path);
  if (signal?.aborted) throw new DOMException("Request canceled", "AbortError");
  const controller = new AbortController();
  const cancel = () => controller.abort();
  signal?.addEventListener("abort", cancel, { once: true });
  let timedOut = false;
  const timeout = setTimeout(() => {
    timedOut = true;
    controller.abort();
  }, PRACTICE_REQUEST_TIMEOUT_MS);
  try {
    const response = await fetch(path, { signal: controller.signal });
    if (!response.ok) {
      if (response.status === 404) {
        throw new PracticeServiceError("This problem could not be found.");
      }
      throw new PracticeServiceError(
        "The practice service is unavailable. Please try again.",
      );
    }
    let payload: unknown;
    try {
      payload = await response.json();
    } catch (error) {
      if (controller.signal.aborted) throw error;
      throw invalidResponse();
    }
    const result = schema.safeParse(payload);
    if (!result.success) throw invalidResponse();
    return result.data as T;
  } catch (error) {
    // Callers suppress canceled requests when unmounting; a service timeout is
    // a visible retryable failure rather than an AbortError they would ignore.
    if (signal?.aborted)
      throw new DOMException("Request canceled", "AbortError");
    if (timedOut) {
      throw new PracticeServiceError(
        "The practice service took too long to respond. Please try again.",
      );
    }
    if (error instanceof PracticeServiceError) throw error;
    throw new PracticeServiceError(
      "The practice service is unavailable. Please try again.",
    );
  } finally {
    clearTimeout(timeout);
    signal?.removeEventListener("abort", cancel);
  }
}
