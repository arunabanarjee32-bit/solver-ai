"use client";

import Link from "next/link";
import { useEffect, useRef, useState } from "react";
import { authClient } from "@/features/accounts/client";
import {
  requestAccountHint,
  type HintLevel,
  type HintResponse,
} from "@/features/hints/api";

const provenanceLabels = {
  authored: "Author-written · not AI-generated",
  mock: "Mock response · not AI-generated",
  model: "AI-generated hint",
} as const;

/** Optional account API, separate from the existing public authored hint ladder. */
export function AccountHint({
  slug,
  level,
}: {
  slug: string;
  level: HintLevel;
}) {
  const { data: session, isPending } = authClient.useSession();
  const [result, setResult] = useState<HintResponse | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const active = useRef<AbortController | null>(null);

  useEffect(() => {
    active.current?.abort();
    active.current = null;
    setResult(null);
    setError("");
    setLoading(false);
    return () => {
      active.current?.abort();
      active.current = null;
    };
  }, [slug, level, session?.user.id]);

  async function loadHint() {
    if (!session || isPending || active.current) return;
    const controller = new AbortController();
    active.current = controller;
    setLoading(true);
    setResult(null);
    setError("");
    try {
      const response = await requestAccountHint(
        { problem_slug: slug, level },
        controller.signal,
      );
      if (!controller.signal.aborted) setResult(response);
    } catch (failure) {
      if (!controller.signal.aborted) {
        setError(
          failure instanceof Error
            ? failure.message
            : "The hint service is unavailable.",
        );
      }
    } finally {
      if (active.current === controller) {
        active.current = null;
        setLoading(false);
      }
    }
  }

  function cancel() {
    active.current?.abort();
    active.current = null;
    setLoading(false);
  }

  return (
    <section className="account-hint" aria-label="Account hint service">
      <h3>Account hint service</h3>
      <p className="account-hint-note">
        Optional signed-in API request for level {level}. The service currently
        returns author-written hints, not AI-generated help. The public hints
        above remain available without signing in.
      </p>
      {!isPending && !session ? (
        <p>
          <Link
            className="inline-link"
            href={"/account?next=" + encodeURIComponent("/problems/" + slug)}
          >
            Sign in to request a hint from the account service.
          </Link>
        </p>
      ) : (
        <div className="account-hint-actions">
          <button
            type="button"
            className="button secondary"
            disabled={isPending || loading || !session}
            onClick={() => void loadHint()}
          >
            {loading
              ? "Requesting hint…"
              : error
                ? "Retry account hint"
                : "Request level " + level + " hint"}
          </button>
          {loading && (
            <button type="button" className="text-button" onClick={cancel}>
              Cancel request
            </button>
          )}
        </div>
      )}
      {loading && <p role="status">Loading your account hint…</p>}
      {error && (
        <p className="form-error" role="alert">
          {error}
        </p>
      )}
      {result && session && (
        <div className="hint account-hint-output" aria-live="polite">
          <span>
            LEVEL {result.level} · {provenanceLabels[result.source]}
            {result.provider ? " · " + result.provider : ""}
          </span>
          <p>{result.hint}</p>
        </div>
      )}
    </section>
  );
}
