// Run before starting Next.js. Use the dependency's schema/migration code rather
// than maintaining a parallel copy of its session/account/JWKS tables.
import { fileURLToPath } from "node:url";
import { getMigrations } from "better-auth/db/migration";
import { getAuthOptions } from "../lib/auth.ts";

process.chdir(fileURLToPath(new URL("../", import.meta.url)));
const options = getAuthOptions();
try {
  const migrations = await getMigrations(options);
  await migrations.runMigrations();
  console.log("Authentication schema is ready.");
} finally {
  options.database.close();
}
