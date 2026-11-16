"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useState } from "react";
import { authClient } from "@/features/accounts/client";
import { Icon } from "./icons";
export function Shell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const { data: session, isPending } = authClient.useSession();
  const [signingOut, setSigningOut] = useState(false);
  const [error, setError] = useState("");
  async function signOut() {
    setSigningOut(true);
    setError("");
    try {
      const result = await authClient.signOut();
      if (result.error) setError("Sign out failed. Try again.");
      else {
        router.replace("/");
        router.refresh();
      }
    } catch {
      setError("Sign out failed. Try again.");
    } finally {
      setSigningOut(false);
    }
  }
  return (
    <div className="app-shell">
      <a className="skip-link" href="#main">
        Skip to content
      </a>
      <aside className="sidebar">
        <Link href="/" className="brand" aria-label="Solver AI home">
          <span className="brand-mark">
            <Icon name="code" size={22} />
          </span>
          solver<span className="brand-ai">ai</span>
          <span className="brand-dot" />
        </Link>
        <div className="workspace-label">YOUR WORKSPACE</div>
        <nav aria-label="Main navigation">
          <Link
            href="/"
            aria-current={
              pathname === "/" || pathname.startsWith("/problems/")
                ? "page"
                : undefined
            }
            className={`nav-item ${pathname === "/" || pathname.startsWith("/problems/") ? "active" : ""}`}
          >
            <Icon name="grid" />
            Practice
            <span className="nav-pip" />
          </Link>
          <Link
            href="/submissions"
            aria-current={pathname === "/submissions" ? "page" : undefined}
            className={`nav-item ${pathname === "/submissions" ? "active" : ""}`}
          >
            <Icon name="book" />
            Submissions
          </Link>
          <Link
            href="/account"
            aria-current={pathname === "/account" ? "page" : undefined}
            className={`nav-item ${pathname === "/account" ? "active" : ""}`}
          >
            <Icon name="code" />
            {session ? "Account" : "Sign in"}
          </Link>
        </nav>
        <div className="sidebar-note">
          <div className="note-icon">
            <Icon name="spark" size={22} />
          </div>
          <strong>One problem at a time.</strong>
          <p>
            Build intuition. Explore ideas.
            <br />
            Make the next connection.
          </p>
          <span className="mini-tag">EARLY DEVELOPMENT</span>
        </div>
        <div className="sidebar-footer">
          <span className="avatar">S</span>
          <div>
            <strong>
              {isPending
                ? "Checking account…"
                : session?.user.name || "Local workspace"}
            </strong>
            <span>{session ? "Signed in" : "Browsing without an account"}</span>
            {session && (
              <button
                className="text-button sidebar-signout"
                disabled={signingOut}
                onClick={() => void signOut()}
              >
                Sign out
              </button>
            )}
            {error && <span role="alert">{error}</span>}
          </div>
        </div>
      </aside>
      <div className="main-shell">
        <header className="topbar">
          <span>
            Practice <span className="topbar-slash">/</span>{" "}
            <strong>Your next breakthrough</strong>
          </span>
          <span className="build-label">
            <span />
            Development preview
          </span>
        </header>
        <main id="main">{children}</main>
        <footer className="footer">
          <span>Built for the way you learn.</span>
          <span>
            Solver AI <span className="footer-dot">·</span> Original problems,
            private submission history.
          </span>
        </footer>
      </div>
    </div>
  );
}
