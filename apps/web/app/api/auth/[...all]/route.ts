import { toNextJsHandler } from "better-auth/next-js";
import { ensureAuthReady, getAuth } from "@/features/accounts/server";

export const runtime = "nodejs";

// Keep Better Auth's HTTP origin, CSRF and rate checks on every auth operation.
export const { GET, POST } = toNextJsHandler(async (request) => {
  await ensureAuthReady();
  return getAuth().handler(request);
});
