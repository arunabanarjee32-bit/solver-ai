"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { authClient } from "@/features/accounts/client";

function safeNext(value: string) {
  if (
    !value.startsWith("/") ||
    value.startsWith("//") ||
    value.includes("\\") ||
    Array.from(value).some((character) => character.charCodeAt(0) < 32)
  )
    return "/";
  try {
    const target = new URL(value, window.location.origin);
    return target.origin === window.location.origin
      ? `${target.pathname}${target.search}${target.hash}`
      : "/";
  } catch {
    return "/";
  }
}

export function AccountForm({ nextPath = "/" }: { nextPath?: string }) {
  const router = useRouter();
  const { data: session, isPending } = authClient.useSession();
  const [mode, setMode] = useState<"signin" | "signup">("signin");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setBusy(true);
    setError("");
    try {
      const result =
        mode === "signup"
          ? await authClient.signUp.email({
              email,
              password,
              name: name.trim(),
            })
          : await authClient.signIn.email({ email, password });
      if (result.error) {
        setError(
          mode === "signup"
            ? "We could not create this account. Check your details or sign in if you already have one."
            : "We could not sign you in. Check your email and password and try again.",
        );
        return;
      }
      setPassword("");
      router.replace(safeNext(nextPath));
      router.refresh();
    } catch {
      setError("The account service is unavailable. Please try again.");
    } finally {
      setBusy(false);
    }
  }
  return (
    <section className="account-page">
      <span className="section-eyebrow">A SPACE FOR YOUR PRACTICE</span>
      <h1>
        {session
          ? "Your account"
          : mode === "signup"
            ? "Make room for progress."
            : "Welcome back."}
      </h1>
      <p className="account-intro">
        Browse and edit without an account. Sign in to run code, submit
        solutions, and keep your submission history.
      </p>
      {isPending ? (
        <div className="state-box" role="status">
          Checking your session…
        </div>
      ) : session ? (
        <div className="account-card">
          <h2>Signed in as {session.user.name}</h2>
          <p>{session.user.email}</p>
          <div className="account-buttons">
            <Link className="button" href="/submissions">
              View submissions
            </Link>
            <button
              className="button secondary"
              disabled={busy}
              onClick={async () => {
                setBusy(true);
                setError("");
                try {
                  const result = await authClient.signOut();
                  if (result.error)
                    setError("We could not sign you out. Please try again.");
                  else router.refresh();
                } catch {
                  setError("We could not sign you out. Please try again.");
                } finally {
                  setBusy(false);
                }
              }}
            >
              Sign out
            </button>
          </div>
          {error && (
            <p className="form-error" role="alert">
              {error}
            </p>
          )}
        </div>
      ) : (
        <div className="account-card">
          <div className="account-tabs" aria-label="Account action">
            <button
              type="button"
              aria-pressed={mode === "signin"}
              onClick={() => {
                setMode("signin");
                setError("");
              }}
            >
              Sign in
            </button>
            <button
              type="button"
              aria-pressed={mode === "signup"}
              onClick={() => {
                setMode("signup");
                setError("");
              }}
            >
              Create account
            </button>
          </div>
          <form onSubmit={submit}>
            {mode === "signup" && (
              <label>
                Display name
                <input
                  name="name"
                  autoComplete="name"
                  value={name}
                  onChange={(event) => setName(event.target.value)}
                  required
                  minLength={1}
                  maxLength={100}
                />
              </label>
            )}
            <label>
              Email address
              <input
                name="email"
                type="email"
                autoComplete="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                required
                maxLength={254}
              />
            </label>
            <label>
              Password
              <input
                name="password"
                type="password"
                autoComplete={
                  mode === "signup" ? "new-password" : "current-password"
                }
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                required
                minLength={12}
                maxLength={128}
              />
            </label>
            <p className="field-note">
              Use 12–128 characters. Passwords are handled by Better Auth.
            </p>
            {error && (
              <p className="form-error" role="alert">
                {error}
              </p>
            )}
            <button
              className="button account-submit"
              type="submit"
              disabled={busy}
            >
              {busy
                ? "Please wait…"
                : mode === "signup"
                  ? "Create your account"
                  : "Sign in to Solver AI"}
            </button>
          </form>
        </div>
      )}
      <p className="account-disclosure">
        Development accounts use email and password. Email ownership is not
        verified in this local setup. Browser drafts stay in this browser;
        source code is sent only when you choose Run or Submit.
      </p>
    </section>
  );
}
