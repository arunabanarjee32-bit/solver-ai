import { randomBytes } from "node:crypto";
import { chmodSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { betterAuth, type BetterAuthOptions } from "better-auth";
import { getMigrations } from "better-auth/db/migration";
import { jwt } from "better-auth/plugins";

/** The web service is the sole session authority; the API verifies its JWKS. */
function authOrigin(): string {
  const url = new URL(process.env.AUTH_URL || "http://127.0.0.1:3000");
  if (
    !["http:", "https:"].includes(url.protocol) ||
    url.username ||
    url.password ||
    url.pathname !== "/" ||
    url.search ||
    url.hash
  ) {
    throw new Error(
      "AUTH_URL must be an HTTP(S) origin without credentials or a path.",
    );
  }
  const loopback = ["127.0.0.1", "localhost", "[::1]"].includes(url.hostname);
  if (url.protocol !== "https:" && !loopback) {
    throw new Error(
      "AUTH_URL must use HTTPS outside a local loopback workspace.",
    );
  }
  return url.origin;
}

/** Generate a workspace key once; never rely on the library's public dev key. */
function authSecret(path: string): string {
  const supplied = process.env.BETTER_AUTH_SECRET;
  if (supplied !== undefined) {
    if (supplied.length < 32) {
      throw new Error(
        "BETTER_AUTH_SECRET must contain at least 32 characters.",
      );
    }
    return supplied;
  }
  mkdirSync(dirname(path), { recursive: true, mode: 0o700 });
  let secret: string;
  try {
    secret = readFileSync(path, "utf8").trim();
  } catch (error) {
    if ((error as NodeJS.ErrnoException).code !== "ENOENT") throw error;
    const generated = randomBytes(32).toString("base64url");
    try {
      writeFileSync(path, `${generated}\n`, { flag: "wx", mode: 0o600 });
    } catch (writeError) {
      // A second process can initialize the same new workspace concurrently.
      if ((writeError as NodeJS.ErrnoException).code !== "EEXIST")
        throw writeError;
    }
    secret = readFileSync(path, "utf8").trim();
  }
  if (secret.length < 32) {
    throw new Error(
      "The saved authentication key is invalid; restore the workspace key.",
    );
  }
  chmodSync(path, 0o600);
  return secret;
}

function createAuthOptions() {
  const baseURL = authOrigin();
  const databasePath = resolve(
    /*turbopackIgnore: true*/
    process.env.AUTH_DB_PATH || ".local/auth.sqlite",
  );
  const secretPath = resolve(
    /*turbopackIgnore: true*/
    process.env.AUTH_SECRET_PATH || `${dirname(databasePath)}/auth-secret`,
  );
  const secret = authSecret(secretPath);
  mkdirSync(dirname(databasePath), { recursive: true, mode: 0o700 });
  const database = new DatabaseSync(databasePath);
  // Concurrent tabs/processes can write sessions; keep waits bounded.
  database.exec(
    "PRAGMA journal_mode = WAL; PRAGMA busy_timeout = 5000; PRAGMA foreign_keys = ON;",
  );
  chmodSync(databasePath, 0o600);
  return {
    appName: "Solver AI",
    baseURL,
    secret,
    database,
    trustedOrigins: [baseURL],
    emailAndPassword: {
      enabled: true,
      minPasswordLength: 12,
      maxPasswordLength: 128,
    },
    session: {
      expiresIn: 60 * 60 * 24 * 7,
      updateAge: 60 * 60 * 24,
      cookieCache: { enabled: false },
    },
    rateLimit: {
      enabled: true,
      storage: "database",
      window: 60,
      max: 100,
      customRules: {
        "/sign-in/email": { window: 60, max: 10 },
        "/sign-up/email": { window: 60, max: 10 },
      },
    },
    advanced: {
      useSecureCookies: new URL(baseURL).protocol === "https:",
      defaultCookieAttributes: { httpOnly: true, sameSite: "lax" },
      // Direct local Next.js does not have a trusted ingress. Shared counters
      // are preferable to letting clients choose their own forwarding headers.
      ipAddress: { ipAddressHeaders: [] },
    },
    telemetry: { enabled: false },
    plugins: [
      jwt({
        disableSettingJwtHeader: true,
        jwks: { keyPairConfig: { alg: "EdDSA", crv: "Ed25519" } },
        jwt: {
          issuer: baseURL,
          audience: "solver-api",
          expirationTime: "5m",
          definePayload: () => ({ token_use: "solver_api" }),
        },
      }),
    ],
  } satisfies BetterAuthOptions;
}

function initializeAuth() {
  return betterAuth(getAuthOptions());
}

// Preserve SQLite handles/session authority across development hot reloads.
const authState = globalThis as typeof globalThis & {
  solverAuthOptions?: ReturnType<typeof createAuthOptions>;
  solverAuthInstance?: ReturnType<typeof initializeAuth>;
  solverAuthReady?: Promise<void>;
};

/** Called by the explicit, idempotent migration script as well as the server. */
export function getAuthOptions() {
  authState.solverAuthOptions ??= createAuthOptions();
  return authState.solverAuthOptions;
}

/** Lazy: importing a route during next build never creates a database or key. */
export function getAuth() {
  authState.solverAuthInstance ??= initializeAuth();
  return authState.solverAuthInstance;
}

/** Initialize the supported schema on first runtime use, not during a build. */
export function ensureAuthReady(): Promise<void> {
  if (!authState.solverAuthReady) {
    const attempt = (async () => {
      const migrations = await getMigrations(getAuthOptions());
      await migrations.runMigrations();
    })();
    authState.solverAuthReady = attempt;
    void attempt.catch(() => {
      if (authState.solverAuthReady === attempt)
        authState.solverAuthReady = undefined;
    });
  }
  return authState.solverAuthReady;
}
