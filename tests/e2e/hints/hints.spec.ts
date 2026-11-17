import { expect, test as base, type Page } from "@playwright/test";
import { HINT_REQUEST_TIMEOUT_MS } from "../../../apps/web/features/hints/api";

type HintAccount = { email: string; password: string };

// Hint cases only read public authored content. Reuse account identity per
// worker while each test keeps Playwright's fresh browser context and session.
// The submissions suite independently exercises signup and cross-user ownership.
const test = base.extend<object, { hintAccount: HintAccount }>({
  hintAccount: [
    async ({ playwright }, use, workerInfo) => {
      const baseURL = workerInfo.project.use.baseURL;
      if (!baseURL) throw new Error("The hint fixture requires a configured baseURL.");
      const origin = new URL(baseURL).origin;
      const account = {
        email: "hints-" + crypto.randomUUID() + "@example.test",
        password: "local-hint-password-42",
      };
      const registration = await playwright.request.newContext({
        baseURL,
        extraHTTPHeaders: { Origin: origin },
      });
      try {
        const response = await registration.post("/api/auth/sign-up/email", {
          data: { name: "Hint Learner", ...account },
        });
        expect(response.status(), "Worker hint account registration must succeed").toBe(200);
      } finally {
        // Never reuse the registration cookies as a test's browser session.
        await registration.dispose();
      }
      await use(account);
    },
    { scope: "worker" },
  ],
});

async function signIn(page: Page, account: HintAccount) {
  await page.goto("/account?next=%2Fproblems%2Fsignal-sum");
  await page.getByLabel("Email address", { exact: true }).fill(account.email);
  await page.getByLabel("Password", { exact: true }).fill(account.password);
  await page
    .getByRole("button", { name: "Sign in to Solver AI", exact: true })
    .click();
  await expect(page).toHaveURL(/\/problems\/signal-sum$/);
  await expect(
    page.getByRole("button", { name: "Request level 1 hint" }),
  ).toBeEnabled();
}

test("guest retains free authored hints without submitting a hint API request", async ({
  page,
}) => {
  const requests: string[] = [];
  page.on("request", (request) => {
    if (request.url().includes("/api/v1/hints")) requests.push(request.url());
  });
  await page.goto("/problems/signal-sum");
  await expect(
    page.getByRole("link", { name: "Sign in to request a hint from the account service." }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Reveal first hint" }).click();
  await expect(
    page.getByText("Keep a running total as you visit the readings."),
  ).toBeVisible();
  expect(requests).toEqual([]);
  const unauthorized = await page.request.post("/api/v1/hints", {
    data: { problem_slug: "signal-sum", level: 1 },
  });
  expect(unauthorized.status()).toBe(401);
});

test("signed-in request uses API JWT and labels offline content as authored", async ({
  page,
  hintAccount,
}) => {
  await signIn(page, hintAccount);
  const responsePromise = page.waitForResponse(
    (response) =>
      response.url().endsWith("/api/v1/hints") &&
      response.request().method() === "POST",
  );
  await page.getByRole("button", { name: "Request level 1 hint" }).click();
  const response = await responsePromise;
  expect(response.ok()).toBeTruthy();
  expect(response.request().headers()["authorization"]).toMatch(/^Bearer /);
  expect(response.request().postDataJSON()).toEqual({
    problem_slug: "signal-sum",
    level: 1,
  });
  await expect(page.locator(".account-hint-output")).toContainText(
    "Author-written · not AI-generated",
  );
  await expect(page.locator(".account-hint-output")).toContainText(
    "Keep a running total as you visit the readings.",
  );
  await expect(page.getByText("AI-generated hint", { exact: true })).toHaveCount(0);
  await page.getByRole("button", { name: "Reveal first hint" }).click();
  await page.getByRole("button", { name: "Request level 2 hint" }).click();
  await expect(page.locator(".account-hint-output")).toContainText(
    "LEVEL 2 · Author-written",
  );
});

test("mock provenance is not passed off as AI, but genuine model flag is distinct", async ({
  page,
  hintAccount,
}) => {
  await signIn(page, hintAccount);
  await page.route("**/api/v1/hints", async (route) => {
    const request = route.request().postDataJSON() as {
      problem_slug: string;
      level: number;
    };
    await route.fulfill({
      status: 200,
      json: {
        schema_version: "1",
        problem_slug: request.problem_slug,
        level: request.level,
        hint: "Deterministic fixture hint",
        source: "mock",
        provider: "test-fixture",
        ai_generated: false,
      },
    });
  });
  await page.getByRole("button", { name: "Request level 1 hint" }).click();
  await expect(page.locator(".account-hint-output")).toContainText(
    "Mock response · not AI-generated · test-fixture",
  );
  await page.unroute("**/api/v1/hints");
  await page.route("**/api/v1/hints", async (route) => {
    const request = route.request().postDataJSON() as {
      problem_slug: string;
      level: number;
    };
    await route.fulfill({
      status: 200,
      json: {
        schema_version: "1",
        problem_slug: request.problem_slug,
        level: request.level,
        hint: "Synthetic test-only model answer",
        source: "model",
        provider: "model-fixture",
        ai_generated: true,
      },
    });
  });
  await page.getByRole("button", { name: "Request level 1 hint" }).click();
  await expect(page.locator(".account-hint-output")).toContainText(
    "AI-generated hint · model-fixture",
  );
});

test("invalid provenance, upstream failures and recovery never expose private diagnostics", async ({
  page,
  hintAccount,
}) => {
  await signIn(page, hintAccount);
  await page.route("**/api/v1/hints", (route) =>
    route.fulfill({
      status: 200,
      json: {
        schema_version: "1",
        problem_slug: "signal-sum",
        level: 1,
        hint: "leak-me",
        source: "model",
        provider: null,
        ai_generated: false,
      },
    }),
  );
  await page.getByRole("button", { name: "Request level 1 hint" }).click();
  await expect(page.locator(".account-hint .form-error[role='alert']")).toContainText("invalid response");
  await expect(page.getByText("leak-me")).toHaveCount(0);
  await page.unroute("**/api/v1/hints");
  await page.route("**/api/v1/hints", (route) =>
    route.fulfill({
      status: 503,
      json: {
        error: { code: "HINT_PROVIDER_UNAVAILABLE", message: "internal-secret" },
      },
    }),
  );
  await page.getByRole("button", { name: "Retry account hint" }).click();
  await expect(page.locator(".account-hint .form-error[role='alert']")).toContainText("unavailable");
  await expect(page.getByText("internal-secret")).toHaveCount(0);
  await page.unroute("**/api/v1/hints");
  await page.getByRole("button", { name: "Retry account hint" }).click();
  await expect(page.locator(".account-hint-output")).toContainText(
    "Author-written · not AI-generated",
  );
});

test("stalled request has a visible timeout and remains retryable", async ({
  page,
  hintAccount,
}) => {
  await signIn(page, hintAccount);
  await page.clock.install();
  await page.route("**/api/v1/hints", () => {
    // Keep the request pending; the client's AbortController owns the deadline.
  });
  const sent = page.waitForRequest((request) =>
    request.url().endsWith("/api/v1/hints"),
  );
  await page.getByRole("button", { name: "Request level 1 hint" }).click();
  await sent;
  await expect(page.getByRole("button", { name: "Cancel request" })).toBeVisible();
  await page.clock.fastForward(HINT_REQUEST_TIMEOUT_MS + 1);
  await expect(page.locator(".account-hint .form-error[role='alert']")).toContainText("too long");
  await page.unroute("**/api/v1/hints");
  await page.getByRole("button", { name: "Retry account hint" }).click();
  await expect(page.locator(".account-hint-output")).toContainText(
    "Author-written · not AI-generated",
  );
});

test("canceling an account hint aborts the request and permits a fresh attempt", async ({
  page,
  hintAccount,
}) => {
  await signIn(page, hintAccount);
  await page.route("**/api/v1/hints", () => {
    // Hold the request until the learner explicitly cancels it.
  });
  const sent = page.waitForRequest((request) =>
    request.url().endsWith("/api/v1/hints"),
  );
  await page.getByRole("button", { name: "Request level 1 hint" }).click();
  await sent;
  const aborted = page.waitForEvent("requestfailed", (request) =>
    request.url().endsWith("/api/v1/hints"),
  );
  await page.getByRole("button", { name: "Cancel request" }).click();
  await aborted;
  await expect(page.getByRole("status").filter({ hasText: "Loading your account hint" })).toHaveCount(0);
  await expect(page.locator(".account-hint .form-error")).toHaveCount(0);
  await expect(page.locator(".account-hint-output")).toHaveCount(0);
  await page.unroute("**/api/v1/hints");
  await page.getByRole("button", { name: "Request level 1 hint" }).click();
  await expect(page.locator(".account-hint-output")).toContainText(
    "LEVEL 1 · Author-written",
  );
});

test("changing hint level aborts the old request and releases the next level", async ({
  page,
  hintAccount,
}) => {
  await signIn(page, hintAccount);
  await page.route("**/api/v1/hints", () => {
    // Keep the previous level pending while the learner changes context.
  });
  const sent = page.waitForRequest((request) =>
    request.url().endsWith("/api/v1/hints"),
  );
  await page.getByRole("button", { name: "Request level 1 hint" }).click();
  await sent;
  const aborted = page.waitForEvent("requestfailed", (request) =>
    request.url().endsWith("/api/v1/hints"),
  );
  await page.getByRole("button", { name: "Reveal first hint" }).click();
  await aborted;
  await expect(page.getByRole("button", { name: "Request level 2 hint" })).toBeEnabled();
  await expect(page.locator(".account-hint-output")).toHaveCount(0);
  await page.unroute("**/api/v1/hints");
  await page.getByRole("button", { name: "Request level 2 hint" }).click();
  await expect(page.locator(".account-hint-output")).toContainText(
    "LEVEL 2 · Author-written",
  );
});
