"use client";
import Link from "next/link";
import dynamic from "next/dynamic";
import { useEffect, useState } from "react";
import { getJSON, type Problem } from "@/features/practice/api";
import { Icon } from "@/components/icons";
import { SubmissionPanel } from "@/features/submissions/submission-panel";
import { AccountHint } from "@/features/hints/account-hint";
const CodePane = dynamic(() => import("./code-pane").then((m) => m.CodePane), {
  ssr: false,
  loading: () => (
    <p className="state-box" role="status">
      Loading workspace…
    </p>
  ),
});
export function Workspace({ slug }: { slug: string }) {
  const [problem, setProblem] = useState<Problem | null>(null);
  const [error, setError] = useState("");
  const [retry, setRetry] = useState(0);
  const [language, setLanguage] = useState<"python" | "cpp">("python");
  const [hints, setHints] = useState(0);
  const [source, setSource] = useState("");
  useEffect(() => {
    const controller = new AbortController();
    setProblem(null);
    setError("");
    setHints(0);
    getJSON<Problem>(
      `/api/v1/problems/${encodeURIComponent(slug)}`,
      controller.signal,
    )
      .then(setProblem)
      .catch((err: Error) => {
        if (err.name !== "AbortError") setError(err.message);
      });
    return () => controller.abort();
  }, [slug, retry]);
  return (
    <div className="workspace-page">
      <Link href="/" className="back-link">
        ← Back to problems
      </Link>
      {error ? (
        <div className="state-box" role="alert">
          <h1>We couldn’t open this problem.</h1>
          <p>{error}</p>
          <button className="button" onClick={() => setRetry((n) => n + 1)}>
            Try again
          </button>
        </div>
      ) : !problem ? (
        <div className="state-box" role="status">
          <span className="loader" />
          <p>Opening your workspace…</p>
        </div>
      ) : (
        <>
          <div className="workspace-heading">
            <div>
              <span className="section-eyebrow">YOUR NEXT CHALLENGE</span>
              <h1>{problem.title}</h1>
              <div className="workspace-tags">
                <span
                  className={`difficulty ${problem.difficulty.toLowerCase()}`}
                >
                  <span />
                  {problem.difficulty}
                </span>
                {problem.tags.map((t) => (
                  <span className="topic" key={t}>
                    {t}
                  </span>
                ))}
                <span className="problem-time">
                  <Icon name="clock" size={14} />
                  {problem.estimated_minutes} min
                </span>
              </div>
            </div>
            <span className="workspace-label-right">
              <Icon name="code" size={17} />
              Practice workspace
            </span>
          </div>
          <div className="workspace-columns">
            <article className="statement-panel">
              <div className="panel-top">
                <Icon name="book" size={17} />
                <h2>Problem description</h2>
              </div>
              <div className="statement-content">
                <p className="statement-text">{problem.statement}</p>
                <h3>Input format</h3>
                <p>{problem.input_format}</p>
                <h3>Output format</h3>
                <p>{problem.output_format}</p>
                <h3>Constraints</h3>
                <ul className="constraints">
                  {problem.constraints.map((c) => (
                    <li key={c}>
                      <code>{c}</code>
                    </li>
                  ))}
                </ul>
                <h3>Examples</h3>
                {problem.samples.map((s, i) => (
                  <section
                    className="sample"
                    key={i}
                    aria-label={`Example ${i + 1}`}
                  >
                    <div className="sample-label">EXAMPLE {i + 1}</div>
                    <div className="sample-grid">
                      <div>
                        <h4>Input</h4>
                        <pre>{s.input}</pre>
                      </div>
                      <div>
                        <h4>Output</h4>
                        <pre>{s.output}</pre>
                      </div>
                    </div>
                    <p>
                      <strong>Why it works.</strong> {s.explanation}
                    </p>
                  </section>
                ))}
                <div className="hint-section">
                  <div className="hint-heading">
                    <span>
                      <Icon name="spark" size={18} />
                      <strong>A nudge in the right direction</strong>
                    </span>
                    <span>
                      {hints}/{problem.hints.length}
                    </span>
                  </div>
                  <p>
                    Optional, author-written hints. These are not generated by
                    AI.
                  </p>
                  {problem.hints.slice(0, hints).map((hint, i) => (
                    <div className="hint" key={i}>
                      <span>HINT {i + 1}</span>
                      <p>{hint}</p>
                    </div>
                  ))}
                  {hints < problem.hints.length && (
                    <button
                      className="button secondary"
                      onClick={() => setHints((n) => n + 1)}
                    >
                      Reveal {hints === 0 ? "first" : "next"} hint{" "}
                      <Icon name="arrow" size={15} />
                    </button>
                  )}
                </div>
                <AccountHint
                  slug={slug}
                  level={Math.min(hints + 1, 3) as 1 | 2 | 3}
                />
                <p className="provenance">
                  Original problem · {problem.provenance.author}
                  <br />
                  {problem.provenance.source}
                </p>
              </div>
            </article>
            <section className="editor-panel" aria-label="Solution editor">
              <div className="panel-top">
                <Icon name="code" size={18} />
                <h2>Your solution</h2>
                <label className="language-select">
                  <span className="sr-only">Programming language</span>
                  <select
                    aria-label="Programming language"
                    value={language}
                    onChange={(e) =>
                      setLanguage(e.target.value as "python" | "cpp")
                    }
                  >
                    <option value="python">Python</option>
                    <option value="cpp">C++17</option>
                  </select>
                </label>
              </div>
              <CodePane
                key={`editor:${slug}:${language}`}
                slug={slug}
                language={language}
                starter={problem.starter_code[language]}
                onCodeChange={setSource}
              />
              <SubmissionPanel
                key={`submission:${slug}:${language}`}
                slug={slug}
                language={language}
                source={source}
              />
            </section>
          </div>
        </>
      )}
    </div>
  );
}
