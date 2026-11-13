// Runtime state must never be copied into a distributable Next.js artifact.
import { readdirSync, existsSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const root = fileURLToPath(new URL("../apps/web/.next/standalone/", import.meta.url));
if (!existsSync(root)) throw new Error("Standalone output is missing; build the web app first.");
const forbidden = [];
function visit(directory) {
  for (const entry of readdirSync(directory, { withFileTypes: true })) {
    const path = join(directory, entry.name);
    if (
      [".local", ".git", "auth-secret", "judge-worker-token"].includes(entry.name) ||
      entry.name === ".env" ||
      (entry.name.startsWith(".env.") && entry.name !== ".env.example")
    ) {
      forbidden.push(path.slice(root.length));
    } else if (entry.isDirectory()) visit(path);
  }
}
visit(root);
if (forbidden.length) {
  throw new Error(`Private runtime state in standalone output: ${forbidden.join(", ")}`);
}
console.log("Standalone packaging check passed: no private runtime state.");
