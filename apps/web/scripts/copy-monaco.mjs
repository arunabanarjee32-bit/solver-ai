// Bundle Monaco locally. Its vendored DOMPurify is explicitly replaced with the
// patched dependency so an npm override cannot leave a vulnerable embedded copy.
import { mkdir, writeFile, readFile } from "node:fs/promises";
import { createRequire } from "node:module";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { build } from "esbuild";
const require = createRequire(import.meta.url);
const sanitizer = JSON.parse(
  await readFile(
    join(dirname(require.resolve("dompurify")), "../package.json"),
    "utf8",
  ),
);
if (sanitizer.version !== "3.4.17")
  throw new Error(
    `Expected patched DOMPurify 3.4.17, found ${sanitizer.version}; refresh dependencies`,
  );
const monacoRoot = dirname(dirname(dirname(require.resolve("monaco-editor"))));
const output = fileURLToPath(new URL("../public/monaco/", import.meta.url));
await mkdir(output, { recursive: true });
const sanitizerRoot = dirname(dirname(require.resolve("dompurify")));
await writeFile(
  join(output, "THIRD_PARTY_NOTICES.txt"),
  [
    "Monaco Editor 0.57.0 — Microsoft and contributors",
    await readFile(join(monacoRoot, "LICENSE"), "utf8"),
    await readFile(join(monacoRoot, "ThirdPartyNotices.txt"), "utf8"),
    "DOMPurify 3.4.17 — Cure53 and contributors; Apache-2.0 OR MPL-2.0",
    await readFile(join(sanitizerRoot, "LICENSE"), "utf8"),
    await readFile(join(sanitizerRoot, "LICENSE-MPL"), "utf8"),
  ].join("\n\n"),
);
const patchSanitizer = {
  name: "patched-monaco-sanitizer",
  setup(build) {
    build.onResolve({ filter: /dompurify\/dompurify\.js$/ }, () => ({
      path: require.resolve("dompurify"),
    }));
  },
};
const common = {
  bundle: true,
  minify: true,
  sourcemap: false,
  plugins: [patchSanitizer],
  legalComments: "eof",
  target: "es2020",
  loader: { ".ttf": "file" },
};
await build({
  ...common,
  stdin: {
    contents: "export * from 'monaco-editor';",
    resolveDir: dirname(fileURLToPath(import.meta.url)),
  },
  outfile: join(output, "editor.js"),
  format: "iife",
  globalName: "SolverMonaco",
  metafile: true,
}).then(async (result) => {
  const inputs = Object.keys(result.metafile.inputs);
  if (inputs.some((path) => path.endsWith("/dompurify/dompurify.js")))
    throw new Error("Vendored DOMPurify must not be included");
  if (!inputs.some((path) => path.includes("/dompurify/dist/")))
    throw new Error("Patched DOMPurify must be included");
  await writeFile(
    join(output, "build-info.json"),
    JSON.stringify(
      {
        monaco: "0.57.0",
        sanitizer: `dompurify@${sanitizer.version}`,
        vendoredSanitizerExcluded: true,
      },
      null,
      2,
    ),
  );
});
await build({
  ...common,
  entryPoints: [join(monacoRoot, "esm/vs/editor/editor.worker.js")],
  outfile: join(output, "editor.worker.js"),
  format: "iife",
});
