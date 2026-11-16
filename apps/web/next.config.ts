import type { NextConfig } from "next";
import { resolve } from "node:path";

const nextConfig: NextConfig = {
  poweredByHeader: false,
  output: "standalone",
  outputFileTracingRoot: resolve(process.cwd(), "../.."),
  // Databases and keys are provisioned at runtime, never application artifacts.
  outputFileTracingExcludes: {
    "/*": [
      ".local/**/*",
      "../../.local/**/*",
      "../../services/**/.local/**/*",
      "../../.git/**/*",
      "../../AnalyseFuture/**/*",
      ".env",
      ".env.*",
      "../../.env",
      "../../.env.*",
    ],
  },
  async rewrites() {
    const api = (process.env.API_BASE_URL || "http://127.0.0.1:8000").replace(
      /\/$/,
      "",
    );
    return [{ source: "/api/v1/:path*", destination: `${api}/api/v1/:path*` }];
  },
};
export default nextConfig;
