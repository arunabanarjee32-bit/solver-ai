import { expect, test } from "@playwright/test";
import {
  getJSON,
  PRACTICE_REQUEST_TIMEOUT_MS,
  type ProblemPage,
} from "../../../apps/web/features/practice/api";

const invalidResponse =
  "The practice service returned an invalid response. Please try again.";

test("malformed catalog responses show a safe error and recover on retry", async ({
  page,
}) => {
  const errors: string[] = [];
  page.on("pageerror", (error) => errors.push(error.message));
  await page.route("**/api/v1/problems?*", (route) =>
    route.fulfill({
      status: 200,
      json: {
        items: null,
        total: 3,
        limit: 100,
        offset: 0,
        private_debug: "do-not-echo",
      },
    }),
  );
  await page.goto("/");
  await expect(page.getByText(invalidResponse, { exact: true })).toBeVisible();
  await expect(page.getByText("do-not-echo")).toHaveCount(0);
  expect(errors).toEqual([]);
  await page.unroute("**/api/v1/problems?*");
  await page.getByRole("button", { name: "Try again" }).click();
  await expect(page.getByRole("link", { name: /Signal Sum/ })).toBeVisible();
});

test("malformed problem details are rejected before rendering and can retry", async ({
  page,
}) => {
  const errors: string[] = [];
  page.on("pageerror", (error) => errors.push(error.message));
  await page.route("**/api/v1/problems/signal-sum", async (route) => {
    const response = await route.fetch();
    const problem = await response.json();
    await route.fulfill({
      response,
      json: { ...problem, samples: "not-an-array", starter_code: null },
    });
  });
  await page.goto("/problems/signal-sum");
  await expect(page.getByText(invalidResponse, { exact: true })).toBeVisible();
  await expect(
    page.getByRole("region", { name: "Solution editor" }),
  ).toHaveCount(0);
  expect(errors).toEqual([]);
  await page.unroute("**/api/v1/problems/signal-sum");
  await page.getByRole("button", { name: "Try again" }).click();
  await expect(
    page.getByRole("heading", { name: "Signal Sum", exact: true }),
  ).toBeVisible();
});

test("a stalled catalog request times out visibly and recovers on retry", async ({
  page,
}) => {
  await page.clock.install();
  await page.route("**/api/v1/problems?*", () => {
    // Leave the request pending. The client deadline must abort the fetch.
  });
  const requested = page.waitForRequest((request) =>
    request.url().includes("/api/v1/problems?"),
  );
  await page.goto("/");
  await requested;
  await page.clock.fastForward(PRACTICE_REQUEST_TIMEOUT_MS + 1);
  await expect(
    page.getByText(
      "The practice service took too long to respond. Please try again.",
      { exact: true },
    ),
  ).toBeVisible();
  await page.unroute("**/api/v1/problems?*");
  await page.getByRole("button", { name: "Try again" }).click();
  await expect(page.getByRole("link", { name: /Signal Sum/ })).toBeVisible();
});

test("an external cancellation remains AbortError and cancels the underlying fetch", async () => {
  const originalFetch = globalThis.fetch;
  let requestSignal: AbortSignal | null | undefined;
  globalThis.fetch = async (_input, init) => {
    requestSignal = init?.signal;
    return new Promise<Response>((_resolve, reject) => {
      requestSignal?.addEventListener(
        "abort",
        () => {
          reject(new DOMException("Canceled", "AbortError"));
        },
        { once: true },
      );
    });
  };
  try {
    const controller = new AbortController();
    const pending = getJSON<ProblemPage>("/api/v1/problems", controller.signal);
    controller.abort();
    await expect(pending).rejects.toMatchObject({ name: "AbortError" });
    expect(requestSignal?.aborted).toBe(true);
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("an already canceled request never starts a fetch", async () => {
  const originalFetch = globalThis.fetch;
  let requests = 0;
  globalThis.fetch = async () => {
    requests += 1;
    return new Response("{}");
  };
  try {
    const controller = new AbortController();
    controller.abort();
    await expect(
      getJSON("/api/v1/problems", controller.signal),
    ).rejects.toMatchObject({ name: "AbortError" });
    expect(requests).toBe(0);
  } finally {
    globalThis.fetch = originalFetch;
  }
});

test("valid JSON with an invalid summary or count is not trusted", async () => {
  const originalFetch = globalThis.fetch;
  const invalidBodies = [
    { items: [], total: -1, limit: 20, offset: 0 },
    { items: [{ title: "Missing fields" }], total: 1, limit: 20, offset: 0 },
    { items: [], total: 0, limit: 0, offset: 0 },
  ];
  try {
    for (const body of invalidBodies) {
      globalThis.fetch = async () => Response.json(body);
      await expect(getJSON("/api/v1/problems")).rejects.toThrow(
        invalidResponse,
      );
    }
    globalThis.fetch = async () =>
      new Response("<html>private upstream debug</html>");
    await expect(getJSON("/api/v1/problems")).rejects.toThrow(invalidResponse);
  } finally {
    globalThis.fetch = originalFetch;
  }
});
