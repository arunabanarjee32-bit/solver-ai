import { z } from "zod";
import { authClient } from "@/features/accounts/client";

const languageSchema = z.enum(["python", "cpp"]);
const verdictSchema = z.enum([
  "AC",
  "WA",
  "CE",
  "RE",
  "TLE",
  "MLE",
  "OLE",
  "SYSTEM_ERROR",
]);
const submissionSummarySchema = z.object({
  id: z.string().min(1).max(100),
  status: z.enum(["QUEUED", "RUNNING", "FINISHED"]),
  verdict: verdictSchema.nullable(),
  mode: z.enum(["run", "submit"]),
  problem_slug: z.string().min(1).max(100),
  problem_title: z.string().min(1).max(200),
  language: languageSchema,
  created_at: z.iso.datetime({ offset: true }),
  completed_at: z.iso.datetime({ offset: true }).nullable(),
  summary: z.string().max(2_000).nullable(),
});
const submissionSchema = submissionSummarySchema.extend({
  source_code: z.string().max(32_768),
});
const submissionPageSchema = z.object({
  items: z.array(submissionSummarySchema).max(100),
  total: z.number().int().nonnegative(),
  limit: z.number().int().min(1).max(100),
  offset: z.number().int().nonnegative(),
});
const capabilitiesSchema = z.object({
  judge_available: z.boolean(),
  languages: z.array(languageSchema).max(2),
  reason: z.string().max(2_000).nullable(),
});
export type Submission = z.infer<typeof submissionSchema>;
export type SubmissionSummary = z.infer<typeof submissionSummarySchema>;
export type SubmissionPage = z.infer<typeof submissionPageSchema>;
export type Capabilities = z.infer<typeof capabilitiesSchema>;
export type Language = z.infer<typeof languageSchema>;
export type SubmissionMode = "run" | "submit";

export class SubmissionError extends Error {
  constructor(
    message: string,
    public code: string,
    public status: number,
  ) {
    super(message);
  }
}

const errorMessages: Record<string, string> = {
  JUDGE_UNAVAILABLE:
    "The judge is unavailable. Your draft is safe; try again after the worker starts.",
  SUBMISSION_IN_PROGRESS:
    "You already have an active job. Check your submission history before trying again.",
  RATE_LIMITED:
    "You have reached the submission limit. Wait a minute before trying again.",
  IDEMPOTENCY_CONFLICT:
    "This request changed while being retried. Try submitting a new draft.",
  PROBLEM_NOT_FOUND: "This problem is no longer available.",
  NOT_FOUND: "This submission could not be found.",
  SUBMISSION_NOT_FOUND: "This submission could not be found.",
  QUEUE_FULL: "The judge queue is full. Your draft is safe; try again shortly.",
  INVALID_REQUEST:
    "The submission was not accepted. Check the language and source size.",
};

async function request<T>(
  path: string,
  schema: z.ZodType<T>,
  options: {
    signal?: AbortSignal;
    body?: unknown;
    idempotencyKey?: string;
    authenticated?: boolean;
  } = {},
): Promise<T> {
  const controller = new AbortController();
  const cancel = () => controller.abort();
  if (options.signal?.aborted)
    throw new DOMException("Request canceled", "AbortError");
  options.signal?.addEventListener("abort", cancel, { once: true });
  let timedOut = false;
  const timeout = setTimeout(() => {
    timedOut = true;
    controller.abort();
  }, 15_000);
  try {
    const headers: Record<string, string> = {};
    if (options.authenticated !== false) {
      // The short-lived token is fetched for this request and never persisted.
      const result = await authClient.token({
        fetchOptions: { signal: controller.signal },
      });
      if (result.error || !result.data?.token) {
        throw new SubmissionError(
          "Sign in again to continue.",
          "AUTH_REQUIRED",
          401,
        );
      }
      headers.Authorization = `Bearer ${result.data.token}`;
    }
    if (options.body !== undefined)
      headers["Content-Type"] = "application/json";
    if (options.idempotencyKey)
      headers["Idempotency-Key"] = options.idempotencyKey;
    const response = await fetch(path, {
      method: options.body === undefined ? "GET" : "POST",
      headers,
      body:
        options.body === undefined ? undefined : JSON.stringify(options.body),
      signal: controller.signal,
      cache: "no-store",
    });
    let payload: unknown;
    try {
      payload = await response.json();
    } catch (error) {
      if (controller.signal.aborted) throw error;
      throw new SubmissionError(
        "The submission service returned an invalid response. Please retry.",
        "INVALID_RESPONSE",
        response.status,
      );
    }
    if (!response.ok) {
      const parsed = z
        .object({ error: z.object({ code: z.string().max(100) }) })
        .safeParse(payload);
      const code = parsed.success ? parsed.data.error.code : "REQUEST_FAILED";
      if (response.status === 401 || response.status === 403) {
        throw new SubmissionError(
          "Your session has expired. Sign in again to continue.",
          "AUTH_REQUIRED",
          response.status,
        );
      }
      throw new SubmissionError(
        errorMessages[code] ||
          "The submission service is unavailable. Please try again.",
        code,
        response.status,
      );
    }
    const parsed = schema.safeParse(payload);
    if (!parsed.success)
      throw new SubmissionError(
        "The submission service returned an invalid response. Please retry.",
        "INVALID_RESPONSE",
        response.status,
      );
    return parsed.data;
  } catch (error) {
    if (options.signal?.aborted)
      throw new DOMException("Request canceled", "AbortError");
    if (timedOut)
      throw new SubmissionError(
        "The submission service took too long to respond. Your draft is safe; retry to check the request.",
        "TIMEOUT",
        0,
      );
    if (error instanceof SubmissionError) throw error;
    throw new SubmissionError(
      "The submission service is unavailable. Please try again.",
      "NETWORK_ERROR",
      0,
    );
  } finally {
    clearTimeout(timeout);
    options.signal?.removeEventListener("abort", cancel);
  }
}

export function getCapabilities(signal?: AbortSignal) {
  return request("/api/v1/capabilities", capabilitiesSchema, {
    signal,
    authenticated: false,
  });
}
export function createSubmission(
  input: {
    problem_slug: string;
    language: Language;
    source_code: string;
    mode: SubmissionMode;
  },
  idempotencyKey: string,
  signal?: AbortSignal,
) {
  return request("/api/v1/submissions", submissionSchema, {
    body: input,
    idempotencyKey,
    signal,
  });
}
export function getSubmission(id: string, signal?: AbortSignal) {
  return request(
    `/api/v1/submissions/${encodeURIComponent(id)}`,
    submissionSchema,
    { signal },
  );
}
export function listSubmissions(offset = 0, signal?: AbortSignal) {
  return request(
    `/api/v1/submissions?limit=20&offset=${offset}`,
    submissionPageSchema,
    { signal },
  );
}
