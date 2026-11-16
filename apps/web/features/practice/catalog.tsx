"use client";
import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { getJSON, type ProblemPage } from "@/features/practice/api";
import { Icon } from "@/components/icons";

export function Catalog() {
  const [data, setData] = useState<ProblemPage | null>(null);
  const [error, setError] = useState("");
  const [retry, setRetry] = useState(0);
  const [search, setSearch] = useState("");
  const [difficulty, setDifficulty] = useState("All difficulties");
  const [topic, setTopic] = useState("All topics");
  useEffect(() => {
    const controller = new AbortController();
    setData(null);
    setError("");
    getJSON<ProblemPage>("/api/v1/problems?limit=100", controller.signal)
      .then(setData)
      .catch((err: Error) => {
        if (err.name !== "AbortError") setError(err.message);
      });
    return () => controller.abort();
  }, [retry]);
  const topics = useMemo(
    () => [...new Set(data?.items.flatMap((p) => p.tags) || [])].sort(),
    [data],
  );
  const items = useMemo(
    () =>
      data?.items.filter(
        (p) =>
          (difficulty === "All difficulties" || p.difficulty === difficulty) &&
          (topic === "All topics" || p.tags.includes(topic)) &&
          `${p.title} ${p.summary} ${p.tags.join(" ")}`
            .toLowerCase()
            .includes(search.trim().toLowerCase()),
      ) || [],
    [data, search, difficulty, topic],
  );
  function clear() {
    setSearch("");
    setDifficulty("All difficulties");
    setTopic("All topics");
  }
  return (
    <div className="catalog-page">
      <div className="page-kicker">
        <span className="kicker-line" />
        THE PRACTICE ROOM
      </div>
      <section className="hero">
        <div>
          <h1>
            A little practice.
            <br />
            <span>A lot of possibility.</span>
          </h1>
          <p>
            Great problem solvers aren’t born. They’re built.
            <br className="desktop-break" /> Find your next challenge and work
            through the why.
          </p>
          <a href="#problem-library" className="button">
            Find a problem <Icon name="arrow" size={18} />
          </a>
        </div>
        <div className="hero-art" aria-hidden="true">
          <div className="art-grid" />
          <div className="orbit orbit-one" />
          <div className="orbit orbit-two" />
          <div className="art-block block-one">{"{"}</div>
          <div className="art-block block-two">{"}"}</div>
          <div className="art-code">
            <span className="code-dot" />
            <span>think</span>
            <span className="code-slash">→</span>
            <span>solve</span>
            <span className="code-slash">→</span>
            <span>grow</span>
          </div>
          <span className="art-spark spark-one">✳</span>
          <span className="art-spark spark-two">+</span>
        </div>
      </section>
      <section className="catalog-meta" aria-label="Library details">
        <div>
          <span className="meta-icon">
            <Icon name="code" />
          </span>
          <div>
            <strong>
              {data ? `${data.total} original problems` : "Original problems"}
            </strong>
            <span>Small challenges. Lasting intuition.</span>
          </div>
        </div>
        <div>
          <span className="meta-icon">
            <Icon name="book" />
          </span>
          <div>
            <strong>
              {data
                ? `${topics.length} topics to explore`
                : "Algorithm foundations"}
            </strong>
            <span>Start with the fundamentals.</span>
          </div>
        </div>
        <div>
          <span className="meta-icon">
            <Icon name="spark" />
          </span>
          <div>
            <strong>Your own pace</strong>
            <span>A focused space to think and write.</span>
          </div>
        </div>
      </section>
      <section id="problem-library" className="library">
        <div className="section-heading">
          <div>
            <span className="section-eyebrow">A GOOD PLACE TO START</span>
            <h2>
              Choose your next challenge<span className="heading-dot">.</span>
            </h2>
          </div>
          <span className="library-count">
            {data
              ? `${data.total} problems in the collection`
              : "Loading collection"}
          </span>
        </div>
        <div className="filters">
          <div className="search-field">
            <Icon name="search" size={18} />
            <input
              aria-label="Search problems"
              placeholder="Search problems or topics..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
            {search && (
              <button
                className="search-clear"
                aria-label="Clear search"
                onClick={() => setSearch("")}
              >
                ×
              </button>
            )}
          </div>
          <label className="select-wrap">
            <span className="sr-only">Difficulty</span>
            <select
              aria-label="Difficulty"
              value={difficulty}
              onChange={(e) => setDifficulty(e.target.value)}
            >
              <option>All difficulties</option>
              <option>Easy</option>
              <option>Medium</option>
            </select>
          </label>
          <label className="select-wrap">
            <span className="sr-only">Topic</span>
            <select
              aria-label="Topic"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
            >
              <option>All topics</option>
              {topics.map((t) => (
                <option key={t}>{t}</option>
              ))}
            </select>
          </label>
        </div>
        {error ? (
          <div className="state-box" role="alert">
            <h3>Let’s reconnect.</h3>
            <p>{error}</p>
            <button className="button" onClick={() => setRetry((n) => n + 1)}>
              Try again
            </button>
          </div>
        ) : !data ? (
          <div className="state-box" role="status">
            <span className="loader" />
            <p>Finding your next challenge…</p>
          </div>
        ) : items.length === 0 ? (
          <div className="state-box">
            <h3>No problems found</h3>
            <p>Try a different search or explore all the problems.</p>
            <button className="button secondary" onClick={clear}>
              Clear filters
            </button>
          </div>
        ) : (
          <div className="problem-table">
            <div className="table-heading">
              <span>PROBLEM</span>
              <span>DIFFICULTY</span>
              <span>TOPICS</span>
              <span>TIME</span>
              <span />
            </div>
            {items.map((p, index) => (
              <Link
                href={`/problems/${p.slug}`}
                key={p.id}
                className="problem-row"
              >
                <div className="problem-title-cell">
                  <span className="problem-index">
                    {String(index + 1).padStart(2, "0")}
                  </span>
                  <div>
                    <h3>{p.title}</h3>
                    <p>{p.summary}</p>
                  </div>
                </div>
                <span className={`difficulty ${p.difficulty.toLowerCase()}`}>
                  <span />
                  {p.difficulty}
                </span>
                <div className="topic-chips">
                  {p.tags.map((t) => (
                    <span key={t}>{t}</span>
                  ))}
                </div>
                <span className="problem-time">
                  <Icon name="clock" size={14} />
                  {p.estimated_minutes} min
                </span>
                <span className="row-arrow">
                  <Icon name="arrow" size={18} />
                </span>
              </Link>
            ))}
          </div>
        )}
        {data && !error && (
          <div className="table-footer">
            <span aria-live="polite">
              Showing {items.length} of {data.total} problems
            </span>
            <span>
              Every expert started somewhere. <Icon name="spark" size={14} />
            </span>
          </div>
        )}
      </section>
      <div className="foundation-banner">
        <span className="banner-symbol">
          <Icon name="code" size={24} />
        </span>
        <div>
          <strong>Make each attempt count.</strong>
          <p>
            Explore original problems and keep drafts locally. Running code
            requires an account and an available isolated judge. AI tutoring
            remains planned.
          </p>
        </div>
        <span className="mini-tag">IN DEVELOPMENT</span>
      </div>
    </div>
  );
}
