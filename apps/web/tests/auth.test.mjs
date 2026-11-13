import assert from "node:assert/strict";
import { randomUUID } from "node:crypto";
import { mkdtempSync, readFileSync, rmSync, statSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { after, before, test } from "node:test";
import { getMigrations } from "better-auth/db/migration";
import { getAuth, getAuthOptions } from "../lib/auth.ts";

const directory = mkdtempSync(join(tmpdir(), "solver-auth-test-"));
const origin = "http://127.0.0.1:3000";
process.env.AUTH_URL = origin;
process.env.AUTH_DB_PATH = join(directory, "auth.sqlite");
process.env.AUTH_SECRET_PATH = join(directory, "auth-secret");
delete process.env.BETTER_AUTH_SECRET;

const email = `${randomUUID()}@example.test`;
const password = "correct-horse-battery-123";
let cookie = "";
let userId = "";

function request(path, method = "GET", body, headers = {}) {
  return getAuth().handler(
    new Request(`${origin}/api/auth${path}`, {
      method,
      headers: {
        Origin: origin,
        ...(body ? { "Content-Type": "application/json" } : {}),
        ...headers,
      },
      ...(body ? { body: JSON.stringify(body) } : {}),
    }),
  );
}

before(async () => {
  const { runMigrations } = await getMigrations(getAuthOptions());
  await runMigrations();
  const repeated = await getMigrations(getAuthOptions());
  await repeated.runMigrations();
});

after(() => {
  getAuthOptions().database.close();
  rmSync(directory, { recursive: true, force: true });
});

test("workspace key is private, persisted and not a shared development fallback", () => {
  const key = readFileSync(process.env.AUTH_SECRET_PATH, "utf8").trim();
  assert.ok(key.length >= 32);
  assert.notEqual(key, "better-auth-secret-12345678901234567890");
  assert.equal(statSync(process.env.AUTH_SECRET_PATH).mode & 0o777, 0o600);
  assert.equal(statSync(process.env.AUTH_DB_PATH).mode & 0o777, 0o600);
});

test("untrusted origins cannot create an account", async () => {
  const response = await request(
    "/sign-up/email",
    "POST",
    {
      name: "Blocked user",
      email: `blocked-${email}`,
      password,
    },
    { Origin: "https://attacker.example" },
  );
  assert.equal(response.status, 403);
  const user = getAuthOptions()
    .database.prepare('SELECT id FROM "user" WHERE email = ?')
    .get(`blocked-${email}`);
  assert.equal(user, undefined);
});

test("signup persists a hashed password and an HttpOnly SameSite session", async () => {
  const response = await request("/sign-up/email", "POST", {
    name: "Learner",
    email,
    password,
  });
  assert.equal(response.status, 200);
  const setCookies = response.headers.getSetCookie();
  const sessionCookie = setCookies.find((value) =>
    value.includes("session_token="),
  );
  assert.ok(sessionCookie);
  assert.match(sessionCookie, /HttpOnly/i);
  assert.match(sessionCookie, /SameSite=Lax/i);
  cookie = setCookies.map((value) => value.split(";")[0]).join("; ");
  const body = await response.json();
  userId = body.user.id;
  assert.equal(body.user.email, email);
  assert.equal(body.user.password, undefined);
  const account = getAuthOptions()
    .database.prepare('SELECT password FROM account WHERE "userId" = ?')
    .get(userId);
  assert.ok(account.password.length > 40);
  assert.notEqual(account.password, password);
});

test("session lookup requires the real cookie, ignoring fabricated identity headers", async () => {
  const anonymous = await request("/get-session", "GET", undefined, {
    "X-User-ID": userId,
  });
  assert.equal(await anonymous.json(), null);
  const session = await request("/get-session", "GET", undefined, {
    Cookie: cookie,
  });
  assert.equal((await session.json()).user.id, userId);
});

test("API token has the minimal fixed claims and a matching public signing key", async () => {
  const response = await request("/token", "GET", undefined, {
    Cookie: cookie,
  });
  assert.equal(response.status, 200);
  const { token } = await response.json();
  const [header, payload] = token
    .split(".")
    .slice(0, 2)
    .map((value) => JSON.parse(Buffer.from(value, "base64url").toString()));
  assert.equal(header.alg, "EdDSA");
  assert.equal(payload.iss, origin);
  assert.equal(payload.aud, "solver-api");
  assert.equal(payload.sub, userId);
  assert.equal(payload.token_use, "solver_api");
  assert.ok(payload.exp - payload.iat <= 300);
  assert.equal(payload.email, undefined);
  assert.equal(payload.name, undefined);
  const keys = await (await request("/jwks")).json();
  assert.ok(
    keys.keys.some(
      (key) => key.kid === header.kid && key.kty === "OKP" && !key.d,
    ),
  );
});

test("cross-site signout is rejected and same-origin signout revokes the session", async () => {
  const crossSite = await request(
    "/sign-out",
    "POST",
    {},
    { Cookie: cookie, Origin: "https://attacker.example" },
  );
  assert.equal(crossSite.status, 403);
  const response = await request("/sign-out", "POST", {}, { Cookie: cookie });
  assert.equal(response.status, 200);
  const session = await request("/get-session", "GET", undefined, {
    Cookie: cookie,
  });
  assert.equal(await session.json(), null);
  const token = await request("/token", "GET", undefined, { Cookie: cookie });
  assert.equal(token.status, 401);
});

test("login throttle cannot be bypassed with spoofed forwarding headers", async () => {
  let limited = false;
  for (let index = 0; index < 12; index += 1) {
    const response = await request(
      "/sign-in/email",
      "POST",
      { email, password: "wrong-password-123" },
      {
        "X-Forwarded-For": `198.51.100.${index + 1}`,
      },
    );
    if (response.status === 429) {
      limited = true;
      break;
    }
    assert.equal(response.status, 401);
  }
  assert.equal(limited, true);
});
