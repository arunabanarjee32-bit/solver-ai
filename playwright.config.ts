import { defineConfig, devices } from "@playwright/test";
import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

// Tests never create accounts or submissions in the developer's saved databases.
const stateDirectory =
  process.env.SOLVER_E2E_STATE_DIR ||
  mkdtempSync(join(tmpdir(), "solver-ai-e2e-"));
process.env.SOLVER_E2E_STATE_DIR = stateDirectory;

export default defineConfig({
  testDir: "./tests/e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  workers: process.env.CI ? 2 : undefined,
  reporter: "list",
  use: {
    baseURL: "http://127.0.0.1:3000",
    trace: "retain-on-failure",
    ...devices["Desktop Chrome"],
    launchOptions: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH
      ? { executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH }
      : {},
  },
  webServer: {
    command:
      process.env.SOLVER_E2E_JUDGE === "1"
        ? "npm run dev:judge"
        : "npm run dev",
    url: "http://127.0.0.1:3000",
    reuseExistingServer: false,
    timeout: 120_000,
    gracefulShutdown: { signal: "SIGTERM", timeout: 25_000 },
    env: {
      NEXT_TELEMETRY_DISABLED: "1",
      AUTH_DB_PATH: join(stateDirectory, "auth.sqlite"),
      AUTH_SECRET_PATH: join(stateDirectory, "auth-secret"),
      SOLVER_DB_PATH: join(stateDirectory, "submissions.sqlite3"),
    },
  },
});
