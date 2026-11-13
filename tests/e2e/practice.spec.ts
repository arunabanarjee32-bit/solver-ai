import { test, expect } from "@playwright/test";

test("catalog is backed by the API and filters combine", async ({ page }) => {
  const response = await page.request.get("/api/v1/problems");
  expect(response.ok()).toBeTruthy();
  expect((await response.json()).total).toBe(3);
  await page.goto("/");
  await expect(page.getByRole("link", { name: /Signal Sum/ })).toBeVisible();
  await expect(page.getByText("Showing 3 of 3 problems")).toBeVisible();
  await page
    .getByRole("combobox", { name: "Difficulty", exact: true })
    .selectOption("Medium");
  await expect(
    page.getByRole("link", { name: /Distinct Stations/ }),
  ).toBeVisible();
  await expect(page.getByRole("link", { name: /Signal Sum/ })).toHaveCount(0);
  await page
    .getByRole("textbox", { name: "Search problems" })
    .fill("no such problem");
  await expect(
    page.getByRole("heading", { name: "No problems found" }),
  ).toBeVisible();
  await page.getByRole("button", { name: "Clear filters" }).click();
  await page
    .getByRole("combobox", { name: "Topic", exact: true })
    .selectOption("Implementation");
  await expect(page.getByText("Showing 1 of 3 problems")).toBeVisible();
});

test("problem page loads local Monaco, reveals authored hints and never runs code", async ({
  page,
}) => {
  const externalRequests: string[] = [];
  page.on("request", (request) => {
    if (
      /^https?:/.test(request.url()) &&
      !request.url().startsWith("http://127.0.0.1:3000")
    ) {
      externalRequests.push(request.url());
    }
  });
  await page.goto("/problems/signal-sum");
  await expect(
    page.getByRole("heading", { name: "Signal Sum", exact: true }),
  ).toBeVisible();
  await expect(
    page.getByRole("region", { name: "Example 1", exact: true }),
  ).toContainText("7");
  await expect(page.locator(".monaco-editor").first()).toBeVisible({
    timeout: 30_000,
  });
  await page.getByRole("textbox", { name: "Code editor", exact: true }).focus();
  await page.keyboard.press("ControlOrMeta+A");
  await page.keyboard.insertText("print(7)");
  await expect
    .poll(() =>
      page.evaluate(() =>
        localStorage.getItem("solver-ai:draft:v1:signal-sum:python"),
      ),
    )
    .toBe("print(7)");
  await page.getByRole("button", { name: "Reveal first hint" }).click();
  await expect(
    page.getByText("Keep a running total as you visit the readings."),
  ).toBeVisible();
  await expect(
    page.getByRole("button", { name: "Run samples" }),
  ).toBeDisabled();
  await expect(
    page.getByRole("button", { name: "Submit solution" }),
  ).toBeDisabled();
  expect(externalRequests).toEqual([]);
});

test("drafts survive reload and stay separate by language and problem", async ({
  page,
}) => {
  await page.goto("/problems/signal-sum");
  await page.getByRole("button", { name: "Use simple editor" }).click();
  const editor = page.getByRole("textbox", {
    name: "Code editor",
    exact: true,
  });
  await editor.fill('print("my saved draft")');
  await expect(
    page.getByText("Saved in this browser", { exact: true }),
  ).toBeVisible();
  await page.reload();
  await page.getByRole("button", { name: "Use simple editor" }).click();
  await expect(editor).toHaveValue('print("my saved draft")');
  await page
    .getByRole("combobox", { name: "Programming language" })
    .selectOption("cpp");
  await page.getByRole("button", { name: "Use simple editor" }).click();
  await expect(editor).toHaveValue(/#include <iostream>/);
  await editor.fill("// separate C++ draft");
  await page
    .getByRole("combobox", { name: "Programming language" })
    .selectOption("python");
  await page.getByRole("button", { name: "Use simple editor" }).click();
  await expect(editor).toHaveValue('print("my saved draft")');
  await page.goto("/problems/steady-climb");
  await page.getByRole("button", { name: "Use simple editor" }).click();
  await expect(editor).not.toHaveValue('print("my saved draft")');
  await expect(editor).toHaveValue(/elevations/);
});

test("API outage has a working retry and missing problems have honest errors", async ({
  page,
}) => {
  await page.route("**/api/v1/problems?*", (route) =>
    route.fulfill({ status: 503, body: "{}" }),
  );
  await page.goto("/");
  await expect(
    page
      .getByRole("alert")
      .filter({ has: page.getByRole("button", { name: "Try again" }) }),
  ).toBeVisible();
  await page.unroute("**/api/v1/problems?*");
  await page.getByRole("button", { name: "Try again" }).click();
  await expect(page.getByRole("link", { name: /Signal Sum/ })).toBeVisible();
  await page.goto("/problems/does-not-exist");
  await expect(
    page.getByText("This problem could not be found.", { exact: true }),
  ).toBeVisible();
});

test("local storage failures do not prevent editing", async ({ page }) => {
  await page.addInitScript(() => {
    Storage.prototype.getItem = () => {
      throw new DOMException("Storage blocked", "SecurityError");
    };
    Storage.prototype.setItem = () => {
      throw new DOMException("Storage blocked", "SecurityError");
    };
  });
  await page.goto("/problems/signal-sum");
  await page.getByRole("button", { name: "Use simple editor" }).click();
  await page
    .getByRole("textbox", { name: "Code editor", exact: true })
    .fill("print(42)");
  await expect(
    page.getByText("Draft could not be saved · copy your code to keep it"),
  ).toBeVisible();
});

test("failed Monaco download falls back and can retry without losing the draft", async ({
  page,
}) => {
  await page.route("**/monaco/editor.js", (route) => route.abort());
  await page.goto("/problems/signal-sum");
  await expect(
    page.getByRole("button", { name: "Retry Monaco editor" }),
  ).toBeVisible();
  await page
    .getByRole("textbox", { name: "Code editor", exact: true })
    .fill("print(23)");
  await page.unroute("**/monaco/editor.js");
  await page.getByRole("button", { name: "Retry Monaco editor" }).click();
  await expect(page.locator(".monaco-editor").first()).toBeVisible({
    timeout: 30_000,
  });
  await expect(page.locator(".monaco-editor .view-lines")).toContainText(
    "print(23)",
  );
  await expect
    .poll(() =>
      page.evaluate(() =>
        localStorage.getItem("solver-ai:draft:v1:signal-sum:python"),
      ),
    )
    .toBe("print(23)");
});

test("practice library fits a narrow screen", async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto("/");
  await expect(page.getByRole("link", { name: /Signal Sum/ })).toBeVisible();
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    ),
  ).toBe(true);
  await page.getByRole("link", { name: /Signal Sum/ }).click();
  await expect(
    page.getByRole("heading", { name: "Signal Sum", exact: true }),
  ).toBeVisible();
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    ),
  ).toBe(true);
});
