"use client";

import Link from "next/link";
import { useEffect, useRef, useState } from "react";
import { authClient } from "@/features/accounts/client";
import {
  getSubmission,
  listSubmissions,
  type Submission,
  type SubmissionPage,
} from "@/features/submissions/api";
import { SubmissionResult } from "./submission-panel";

export function SubmissionHistory() {
  const { data: session, isPending } = authClient.useSession();
  const [loaded, setLoaded] = useState<{
    owner: string;
    page: SubmissionPage;
  } | null>(null);
  const data = loaded?.owner === session?.user.id ? loaded?.page : null;
  const [offset, setOffset] = useState(0);
  const [attempt, setAttempt] = useState(0);
  const [error, setError] = useState("");
  const [saved, setSaved] = useState<{ owner: string; job: Submission } | null>(
    null,
  );
  const selected = saved?.owner === session?.user.id ? saved?.job : null;
  const [detailError, setDetailError] = useState("");
  const [detailLoading, setDetailLoading] = useState(false);
  const detailRequest = useRef<AbortController | null>(null);
  useEffect(() => {
    setOffset(0);
    setSaved(null);
    detailRequest.current?.abort();
    setDetailLoading(false);
    return () => detailRequest.current?.abort();
  }, [session?.user.id]);
  useEffect(() => {
    setLoaded(null);
    detailRequest.current?.abort();
    setDetailLoading(false);
    setError("");
    setSaved(null);
    setDetailError("");
    if (!session) return;
    const controller = new AbortController();
    listSubmissions(offset, controller.signal)
      .then((page) => {
        if (!controller.signal.aborted)
          setLoaded({ owner: session.user.id, page });
      })
      .catch((failure) => {
        if (!controller.signal.aborted)
          setError(
            failure instanceof Error
              ? failure.message
              : "We could not load your submissions.",
          );
      });
    return () => controller.abort();
  }, [session?.user.id, offset, attempt]);
  async function open(id: string) {
    if (!session) return;
    const owner = session.user.id;
    detailRequest.current?.abort();
    const controller = new AbortController();
    detailRequest.current = controller;
    setDetailLoading(true);
    setDetailError("");
    setSaved(null);
    try {
      const attempt = await getSubmission(id, controller.signal);
      if (!controller.signal.aborted) setSaved({ owner, job: attempt });
    } catch (failure) {
      if (!controller.signal.aborted)
        setDetailError(
          failure instanceof Error
            ? failure.message
            : "We could not load this submission.",
        );
    } finally {
      if (!controller.signal.aborted) setDetailLoading(false);
    }
  }
  return (
    <section className="history-page">
      <div className="history-heading">
        <div>
          <span className="section-eyebrow">
            YOUR WORK, ONE ATTEMPT AT A TIME
          </span>
          <h1>
            Submission history<span className="heading-dot">.</span>
          </h1>
        </div>
        {session && (
          <button
            className="button secondary"
            onClick={() => setAttempt((n) => n + 1)}
          >
            Refresh history
          </button>
        )}
      </div>
      <p className="account-intro">
        Sample runs and submissions are private to your account. Open an attempt
        to review its actual result and saved source.
      </p>
      {isPending ? (
        <div className="state-box" role="status">
          Checking your session…
        </div>
      ) : !session ? (
        <div className="state-box">
          <h2>Your attempts belong to you.</h2>
          <p>Sign in to see your submission history.</p>
          <Link className="button" href="/account?next=%2Fsubmissions">
            Sign in to view submissions
          </Link>
        </div>
      ) : error ? (
        <div className="state-box" role="alert">
          <h2>We couldn’t load your history.</h2>
          <p>{error}</p>
          <button className="button" onClick={() => setAttempt((n) => n + 1)}>
            Try again
          </button>
        </div>
      ) : !data ? (
        <div className="state-box" role="status">
          Loading your submissions…
        </div>
      ) : data.items.length === 0 ? (
        <div className="state-box">
          <h2>No submissions yet</h2>
          <p>Your sample runs and submitted solutions will appear here.</p>
          <Link className="button" href="/">
            Find a problem
          </Link>
        </div>
      ) : (
        <>
          <div className="history-list">
            {data.items.map((item) => (
              <button
                key={item.id}
                className="history-row"
                onClick={() => void open(item.id)}
                aria-label={`View ${item.problem_title} ${item.mode === "run" ? "sample run" : "submission"}`}
              >
                <span>
                  <strong>{item.problem_title}</strong>
                  <small>
                    {item.mode === "run" ? "Sample run" : "Submission"} ·{" "}
                    {item.language === "cpp" ? "C++17" : "Python"} ·{" "}
                    {new Date(item.created_at).toLocaleString()}
                  </small>
                </span>
                <span
                  className={`verdict-tag ${item.verdict === "AC" ? "accepted" : ""}`}
                >
                  {item.verdict || item.status}
                </span>
                <span aria-hidden="true">→</span>
              </button>
            ))}
          </div>
          <div className="history-pagination">
            <span>
              Showing {offset + 1}–{offset + data.items.length} of {data.total}
            </span>
            <div>
              <button
                className="button secondary"
                disabled={offset === 0}
                onClick={() => setOffset((n) => Math.max(0, n - 20))}
              >
                Previous
              </button>
              <button
                className="button secondary"
                disabled={offset + data.items.length >= data.total}
                onClick={() => setOffset((n) => n + 20)}
              >
                Next
              </button>
            </div>
          </div>
        </>
      )}
      {detailLoading && <p role="status">Loading the saved attempt…</p>}
      {detailError && (
        <p className="form-error" role="alert">
          {detailError}
        </p>
      )}
      {selected && (
        <section className="saved-attempt" aria-label="Saved attempt">
          <div className="history-heading">
            <h2>{selected.problem_title}</h2>
            <button className="text-button" onClick={() => setSaved(null)}>
              Close attempt
            </button>
          </div>
          <SubmissionResult job={selected} />
          <h3>Submitted source</h3>
          <pre className="saved-source">{selected.source_code}</pre>
          <Link
            className="inline-link"
            href={`/problems/${encodeURIComponent(selected.problem_slug)}`}
          >
            Open problem →
          </Link>
        </section>
      )}
    </section>
  );
}
