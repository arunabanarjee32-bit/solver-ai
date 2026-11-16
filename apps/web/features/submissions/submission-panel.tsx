"use client";

import Link from "next/link";
import { useEffect, useRef, useState } from "react";
import { authClient } from "@/features/accounts/client";
import {
  createSubmission,
  getCapabilities,
  getSubmission,
  type Capabilities,
  type Language,
  type Submission,
  type SubmissionMode,
} from "@/features/submissions/api";
import { Icon } from "@/components/icons";

function pause(milliseconds: number, signal: AbortSignal) {
  return new Promise<void>((resolve, reject) => {
    if (signal.aborted) {
      reject(new DOMException("Canceled", "AbortError"));
      return;
    }
    const cancel = () => {
      clearTimeout(timer);
      reject(new DOMException("Canceled", "AbortError"));
    };
    const timer = setTimeout(() => {
      signal.removeEventListener("abort", cancel);
      resolve();
    }, milliseconds);
    signal.addEventListener("abort", cancel, { once: true });
  });
}

export function SubmissionResult({ job }: { job: Submission }) {
  return (
    <div
      className={`submission-result ${job.verdict === "AC" ? "result-accepted" : ""}`}
      aria-live="polite"
    >
      <div className="result-heading">
        <strong>
          {job.status === "FINISHED"
            ? job.verdict === "AC"
              ? "Accepted"
              : job.verdict?.replaceAll("_", " ") || "Finished"
            : job.status === "RUNNING"
              ? "Running your solution…"
              : "Queued for judging…"}
        </strong>
        <span className="result-mode">
          {job.mode === "run" ? "SAMPLE RUN" : "SUBMISSION"}
        </span>
      </div>
      {job.summary && <p>{job.summary}</p>}
      <div className="result-meta">
        <span>{job.language === "cpp" ? "C++17" : "Python"}</span>
        <span>Job {job.id.slice(0, 8)}</span>
        <Link href="/submissions">View history →</Link>
      </div>
    </div>
  );
}

export function SubmissionPanel({
  slug,
  language,
  source,
}: {
  slug: string;
  language: Language;
  source: string;
}) {
  const { data: session, isPending } = authClient.useSession();
  const [caps, setCaps] = useState<Capabilities | null>(null);
  const [capsError, setCapsError] = useState("");
  const [capsAttempt, setCapsAttempt] = useState(0);
  const [job, setJob] = useState<Submission | null>(null);
  const [jobOwner, setJobOwner] = useState<string | null>(null);
  const [sending, setSending] = useState(false);
  const [polling, setPolling] = useState(false);
  const [pollAttempt, setPollAttempt] = useState(0);
  const [error, setError] = useState("");
  const pending = useRef<{ body: string; key: string } | null>(null);
  const creating = useRef<AbortController | null>(null);
  const sourceBytes = new TextEncoder().encode(source).length;
  const busy = sending || (!!job && job.status !== "FINISHED");
  const available =
    !!caps?.judge_available && !capsError && caps.languages.includes(language);
  useEffect(() => {
    const controller = new AbortController();
    async function refresh() {
      while (!controller.signal.aborted) {
        try {
          const next = await getCapabilities(controller.signal);
          setCaps(next);
          setCapsError("");
        } catch (failure) {
          if (!controller.signal.aborted)
            setCapsError(
              failure instanceof Error
                ? failure.message
                : "The judge status is unavailable.",
            );
        }
        try {
          await pause(10_000, controller.signal);
        } catch {
          return;
        }
      }
    }
    void refresh();
    return () => controller.abort();
  }, [capsAttempt]);
  useEffect(() => {
    setJob(null);
    setJobOwner(null);
    setError("");
    pending.current = null;
    creating.current?.abort();
    setSending(false);
    return () => creating.current?.abort();
  }, [session?.user.id]);
  useEffect(() => {
    if (!job || job.status === "FINISHED") return;
    const id = job.id;
    const controller = new AbortController();
    const deadline = Date.now() + 180_000;
    setPolling(true);
    async function poll() {
      try {
        while (Date.now() < deadline) {
          await pause(1_000, controller.signal);
          const latest = await getSubmission(id, controller.signal);
          if (controller.signal.aborted) return;
          setJob(latest);
          if (latest.status === "FINISHED") return;
        }
        setError(
          "This job is still processing. Check your history or retry the status check; no verdict has been assumed.",
        );
      } catch (failure) {
        if (!controller.signal.aborted)
          setError(
            failure instanceof Error
              ? failure.message
              : "We could not check this job.",
          );
      } finally {
        if (!controller.signal.aborted) setPolling(false);
      }
    }
    void poll();
    return () => controller.abort();
    // Job updates stay in this polling loop; only a new job or explicit retry restarts it.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [job?.id, pollAttempt]);
  async function submit(mode: SubmissionMode) {
    if (
      !available ||
      !session ||
      sending ||
      sourceBytes > 32_768 ||
      !source.trim()
    )
      return;
    const input = { problem_slug: slug, language, source_code: source, mode };
    const body = JSON.stringify(input);
    if (!pending.current || pending.current.body !== body)
      pending.current = { body, key: crypto.randomUUID() };
    setSending(true);
    setError("");
    setJob(null);
    setJobOwner(session.user.id);
    const controller = new AbortController();
    creating.current = controller;
    try {
      const created = await createSubmission(
        input,
        pending.current.key,
        controller.signal,
      );
      if (controller.signal.aborted) return;
      setJob(created);
      pending.current = null;
    } catch (failure) {
      if (!controller.signal.aborted)
        setError(
          failure instanceof Error
            ? failure.message
            : "We could not create this request.",
        );
    } finally {
      if (!controller.signal.aborted) setSending(false);
    }
  }
  return (
    <div className="execution-panel">
      <div className="execution-actions">
        <button
          className="button secondary"
          disabled={
            !available ||
            !session ||
            isPending ||
            busy ||
            sourceBytes > 32_768 ||
            !source.trim()
          }
          aria-describedby="judge-note"
          onClick={() => void submit("run")}
        >
          ▷ Run samples
        </button>
        <button
          className="button"
          disabled={
            !available ||
            !session ||
            isPending ||
            busy ||
            sourceBytes > 32_768 ||
            !source.trim()
          }
          aria-describedby="judge-note"
          onClick={() => void submit("submit")}
        >
          Submit solution <Icon name="arrow" size={16} />
        </button>
      </div>
      <p id="judge-note">
        {!caps ? (
          <strong>{capsError || "Checking judge availability…"}</strong>
        ) : !available ? (
          <>
            <strong>Code execution is currently unavailable.</strong>
            {capsError ||
              caps.reason ||
              "Start the isolated judge worker to enable sample runs and submissions."}
          </>
        ) : !session ? (
          <>
            <strong>Ready when you are.</strong>
            <Link
              className="inline-link"
              href={`/account?next=${encodeURIComponent(`/problems/${slug}`)}`}
            >
              Sign in to run code and submit solutions.
            </Link>
          </>
        ) : (
          <>
            <strong>
              Runs use public samples; submissions use the grading set.
            </strong>
            Your source is sent to the isolated judge only when you choose Run
            or Submit.
          </>
        )}
      </p>
      {(!available || capsError) && (
        <button
          className="text-button"
          onClick={() => setCapsAttempt((n) => n + 1)}
        >
          Refresh judge status
        </button>
      )}
      {sourceBytes > 32_768 && (
        <p className="form-error" role="alert">
          Your source is larger than 32 KiB. Shorten it before running or
          submitting.
        </p>
      )}
      {sending && <p role="status">Sending your request…</p>}
      {error && (
        <p className="form-error" role="alert">
          {error}
        </p>
      )}
      {job && jobOwner === session?.user.id && <SubmissionResult job={job} />}
      {job &&
        jobOwner === session?.user.id &&
        job.status !== "FINISHED" &&
        !polling && (
          <button
            className="button secondary"
            onClick={() => {
              setError("");
              setPollAttempt((n) => n + 1);
            }}
          >
            Retry status check
          </button>
        )}
    </div>
  );
}
