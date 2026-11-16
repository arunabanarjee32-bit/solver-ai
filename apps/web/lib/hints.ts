import { z } from "zod";
import { authClient } from "./auth-client";

// Mirrors the bounded, versioned response in solver_api/hints.py.
// Keep provenance validation client-side: an untrusted proxy or fixture cannot
// turn an authored/mock hint into a claim of actual model inference.
const slugSchema = z
  .string()
  .min(1)
  .max(80)
  .regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/);
const hintLevelSchema = z.union([z.literal(1), z.literal(2), z.literal(3)]);
const hintRequestSchema = z.strictObject({
  problem_slug: slugSchema,
  level: hintLevelSchema,
});
const hintResponseSchema = z
  .strictObject({
    schema_version: z.literal("1"),
    problem_slug: slugSchema,
    level: hintLevelSchema,
    hint: z.string().min(1).max(1600),
    source: z.enum(["authored", "mock", "model"]),
    provider: z.string().min(1).max(80).nullable(),
    ai_generated: z.boolean(),
  })
  .refine(
    (value) =>
      (value.source === "authored") === (value.provider === null) &&
      value.ai_generated === (value.source === "model"),
    "The hint service returned inconsistent provenance.",
  );

export type HintLevel = z.infer<typeof hintLevelSchema>;
export type HintResponse = z.infer<typeof hintResponseSchema>;
export const HINT_REQUEST_TIMEOUT_MS = 10_000;

export class HintServiceError extends Error {
  constructor(
    message: string,
    public code: string,
    public status: number,
  ) {
    super(message);
  }
}

function failed(code: string, status: number): HintServiceError {
  if (status === 401 || status === 403) {
    return new HintServiceError(
      "Your session has expired. Sign in again to request account hints.",
      "AUTH_REQUIRED",
      status,
    );
  }
  if (code === "PROBLEM_NOT_FOUND" || status === 404) {
    return new HintServiceError("This problem is no longer available.", code, status);
  }
  if (code === "HINT_PROVIDER_UNAVAILABLE" || status === 503) {
    return new HintServiceError(
      "The hint service is unavailable. The original hints are still available above.",
      code,
      status,
    );
  }
  if (status === 429) {
    return new HintServiceError(
      "Too many requests. Please retry later.",
      "RATE_LIMITED",
      status,
    );
  }
  return new HintServiceError(
    "The hint service could not complete the request. Please retry.",
    code,
    status,
  );
}

export async function requestAccountHint(
  input: { problem_slug: string; level: HintLevel },
  signal?: AbortSignal,
): Promise<HintResponse> {
  const parsedRequest = hintRequestSchema.safeParse(input);
  if (!parsedRequest.success)
    throw new HintServiceError("Invalid hint request.", "INVALID_REQUEST", 0);
  if (signal?.aborted) throw new DOMException("Request canceled", "AbortError");
  const controller = new AbortController();
  const cancel = () => controller.abort();
  signal?.addEventListener("abort", cancel, { once: true });
  let timedOut = false;
  const timeout = setTimeout(() => {
    timedOut = true;
    controller.abort();
  }, HINT_REQUEST_TIMEOUT_MS);

  try {
    // Reuse the exact short-lived Better Auth -> API JWT boundary already used
    // by submissions. Never persist or expose this token to model providers.
    const credentials = await authClient.token({
      fetchOptions: { signal: controller.signal },
    });
    if (controller.signal.aborted)
      throw new DOMException("Request canceled", "AbortError");
    if (credentials.error || !credentials.data?.token) {
      throw new HintServiceError(
        "Sign in to request account hints.",
        "AUTH_REQUIRED",
        401,
      );
    }
    const response = await fetch("/api/v1/hints", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + credentials.data.token,
      },
      body: JSON.stringify(parsedRequest.data),
      cache: "no-store",
      signal: controller.signal,
    });
    let payload: unknown;
    try {
      payload = await response.json();
    } catch (error) {
      if (controller.signal.aborted) throw error;
      throw new HintServiceError(
        "The hint service returned an invalid response. Please retry.",
        "INVALID_RESPONSE",
        response.status,
      );
    }
    if (!response.ok) {
      const parsedError = z
        .object({ error: z.object({ code: z.string().max(100) }) })
        .safeParse(payload);
      throw failed(
        parsedError.success ? parsedError.data.error.code : "REQUEST_FAILED",
        response.status,
      );
    }
    const parsed = hintResponseSchema.safeParse(payload);
    if (
      !parsed.success ||
      parsed.data.problem_slug !== parsedRequest.data.problem_slug ||
      parsed.data.level !== parsedRequest.data.level
    ) {
      throw new HintServiceError(
        "The hint service returned an invalid response. Please retry.",
        "INVALID_RESPONSE",
        response.status,
      );
    }
    return parsed.data;
  } catch (error) {
    if (signal?.aborted)
      throw new DOMException("Request canceled", "AbortError");
    if (timedOut)
      throw new HintServiceError(
        "The hint service took too long to respond. Please retry.",
        "TIMEOUT",
        0,
      );
    if (error instanceof HintServiceError) throw error;
    throw new HintServiceError(
      "The hint service is unreachable. The original hints are still available above.",
      "NETWORK_ERROR",
      0,
    );
  } finally {
    clearTimeout(timeout);
    signal?.removeEventListener("abort", cancel);
  }
}
