import { expect, test, type Page } from "@playwright/test";

const password = "local-practice-password-42";

async function createAccount(page: Page, next = "/submissions") {
  const email = `practice-${crypto.randomUUID()}@example.test`;
  await page.goto(`/account?next=${encodeURIComponent(next)}`);
  await page
    .getByRole("button", { name: "Create account", exact: true })
    .click();
  await page
    .getByLabel("Display name", { exact: true })
    .fill("Practice Learner");
  await page.getByLabel("Email address", { exact: true }).fill(email);
  await page.getByLabel("Password", { exact: true }).fill(password);
  await page
    .getByRole("button", { name: "Create your account", exact: true })
    .click();
  return email;
}

test("accounts sign up, restore a session, sign out, and sign in to private history", async ({
  page,
}) => {
  await page.goto("/submissions");
  await expect(
    page.getByRole("link", { name: "Sign in to view submissions" }),
  ).toBeVisible();
  const email = await createAccount(page);
  await expect(page).toHaveURL(/\/submissions$/);
  await expect(
    page.getByRole("heading", { name: "No submissions yet", exact: true }),
  ).toBeVisible();
  await page.reload();
  await expect(
    page.getByRole("heading", { name: "No submissions yet", exact: true }),
  ).toBeVisible();
  await page
    .getByRole("button", { name: "Sign out", exact: true })
    .first()
    .click();
  await page.goto("/submissions");
  await expect(
    page.getByRole("link", { name: "Sign in to view submissions" }),
  ).toBeVisible();
  await page.getByRole("link", { name: "Sign in to view submissions" }).click();
  await page.getByLabel("Email address", { exact: true }).fill(email);
  await page.getByLabel("Password", { exact: true }).fill(password);
  await page
    .getByRole("button", { name: "Sign in to Solver AI", exact: true })
    .click();
  await expect(page).toHaveURL(/\/submissions$/);
  await expect(
    page.getByRole("heading", { name: "No submissions yet", exact: true }),
  ).toBeVisible();
});

test("account redirects stay on this site", async ({ page }) => {
  await createAccount(page, "//example.com/steal-session");
  await expect(page).toHaveURL("http://127.0.0.1:3000/");
  await expect(page.getByRole("link", { name: /Signal Sum/ })).toBeVisible();
});

test("editing as a guest never uploads the draft", async ({ page }) => {
  const marker = "browser-only-sensitive-draft";
  const uploads: string[] = [];
  page.on("request", (request) => {
    if (request.postData()?.includes(marker)) uploads.push(request.url());
  });
  await page.goto("/problems/signal-sum");
  await page.getByRole("button", { name: "Use simple editor" }).click();
  await page
    .getByRole("textbox", { name: "Code editor", exact: true })
    .fill(`# ${marker}\nprint(7)`);
  await expect(
    page.getByText("Saved in this browser", { exact: true }),
  ).toBeVisible();
  await expect(
    page.getByRole("button", { name: "Run samples" }),
  ).toBeDisabled();
  await expect(
    page.getByRole("button", { name: "Submit solution" }),
  ).toBeDisabled();
  expect(uploads).toEqual([]);
});

test("an unavailable judge keeps authenticated execution disabled", async ({
  page,
}) => {
  await page.route("**/api/v1/capabilities", (route) =>
    route.fulfill({
      status: 200,
      json: {
        judge_available: false,
        languages: ["python", "cpp"],
        reason: "The isolated worker is offline.",
      },
    }),
  );
  await createAccount(page, "/problems/signal-sum");
  await expect(page).toHaveURL(/\/problems\/signal-sum$/);
  await expect(
    page.getByText("The isolated worker is offline.", { exact: false }),
  ).toBeVisible();
  await expect(
    page.getByRole("button", { name: "Run samples" }),
  ).toBeDisabled();
  await expect(
    page.getByRole("button", { name: "Submit solution" }),
  ).toBeDisabled();
});

test("real isolated runs and submissions persist actual verdicts and private history", async ({
  page,
}) => {
  test.skip(
    process.env.SOLVER_E2E_JUDGE !== "1",
    "Requires the isolated judge worker and runtime images.",
  );
  test.setTimeout(300_000);
  await createAccount(page, "/problems/signal-sum");
  await expect(page).toHaveURL(/\/problems\/signal-sum$/);
  await expect(page.getByRole("button", { name: "Run samples" })).toBeEnabled({
    timeout: 90_000,
  });
  await page.getByRole("button", { name: "Use simple editor" }).click();
  const source =
    "import sys\nvalues = list(map(int, sys.stdin.buffer.read().split()))\nprint(sum(values[1:]))\n";
  await page
    .getByRole("textbox", { name: "Code editor", exact: true })
    .fill(source);
  await page.getByRole("button", { name: "Run samples" }).click();
  await expect(page.locator(".submission-result")).toContainText("Accepted", {
    timeout: 120_000,
  });
  await expect(page.locator(".submission-result")).toContainText("SAMPLE RUN");
  await page.getByRole("button", { name: "Submit solution" }).click();
  await expect(page.locator(".submission-result")).toContainText("SUBMISSION");
  await expect(page.locator(".submission-result")).toContainText("Accepted", {
    timeout: 120_000,
  });
  await page
    .getByRole("textbox", { name: "Code editor", exact: true })
    .fill("print(0)\n");
  await page.getByRole("button", { name: "Submit solution" }).click();
  await expect(page.locator(".submission-result")).toContainText("WA", {
    timeout: 120_000,
  });
  await page.getByRole("link", { name: "Submissions", exact: true }).click();
  await expect(page.locator(".history-row")).toHaveCount(3);
  await page
    .getByRole("button", { name: "View Signal Sum submission", exact: true })
    .first()
    .click();
  await expect(
    page.getByRole("region", { name: "Saved attempt" }),
  ).toContainText("print(0)");
  await page
    .getByRole("button", { name: "Sign out", exact: true })
    .first()
    .click();
  await createAccount(page);
  await expect(
    page.getByRole("heading", { name: "No submissions yet", exact: true }),
  ).toBeVisible();
  await expect(page.locator(".saved-attempt")).toHaveCount(0);
});
