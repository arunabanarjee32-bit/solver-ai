"use client";
import Editor, { loader } from "@monaco-editor/react";
import { useEffect, useRef, useState } from "react";
import type * as Monaco from "monaco-editor";

type EditorWindow = Window & {
  SolverMonaco?: typeof Monaco;
  MonacoEnvironment?: { getWorkerUrl: () => string };
};
let editorLoad: Promise<void> | undefined;
function loadEditor(): Promise<void> {
  if (editorLoad) return editorLoad;
  const attempt = new Promise<void>((resolve, reject) => {
    const editorWindow = window as EditorWindow;
    editorWindow.MonacoEnvironment = {
      getWorkerUrl: () => "/monaco/editor.worker.js",
    };
    const css = document.createElement("link");
    css.rel = "stylesheet";
    css.href = "/monaco/editor.css";
    document.head.appendChild(css);
    const script = document.createElement("script");
    script.src = "/monaco/editor.js";
    const fail = (error: Error) => {
      clearTimeout(timeout);
      script.onload = null;
      script.onerror = null;
      script.remove();
      css.remove();
      reject(error);
    };
    const timeout = window.setTimeout(
      () => fail(new Error("Editor assets took too long to load")),
      15000,
    );
    script.onload = () => {
      if (!editorWindow.SolverMonaco) {
        fail(new Error("Editor failed to initialize"));
        return;
      }
      try {
        loader.config({ monaco: editorWindow.SolverMonaco });
        clearTimeout(timeout);
        resolve();
      } catch {
        fail(new Error("Editor failed to initialize"));
      }
    };
    script.onerror = () => fail(new Error("Editor assets could not be loaded"));
    document.head.appendChild(script);
  });
  editorLoad = attempt;
  // A failed download must not poison later attempts or other problem pages.
  void attempt.catch(() => {
    if (editorLoad === attempt) editorLoad = undefined;
  });
  return attempt;
}
export function CodePane({
  slug,
  language,
  starter,
  onCodeChange,
}: {
  slug: string;
  language: "python" | "cpp";
  starter: string;
  onCodeChange?: (value: string) => void;
}) {
  const [code, setCode] = useState(starter);
  const [ready, setReady] = useState(false);
  const [simple, setSimple] = useState(false);
  const [editorReady, setEditorReady] = useState(false);
  const [editorError, setEditorError] = useState("");
  const [editorLoading, setEditorLoading] = useState(true);
  const [editorAttempt, setEditorAttempt] = useState(0);
  const wantsMonaco = useRef(true);
  useEffect(() => {
    let active = true;
    setEditorError("");
    setEditorLoading(true);
    loadEditor()
      .then(() => {
        if (active) {
          setEditorReady(true);
          setEditorLoading(false);
          if (wantsMonaco.current) setSimple(false);
        }
      })
      .catch((error: Error) => {
        if (active) {
          setEditorError(error.message);
          setEditorLoading(false);
          setSimple(true);
        }
      });
    return () => {
      active = false;
    };
  }, [editorAttempt]);
  function toggleEditor() {
    if (simple && editorError) {
      wantsMonaco.current = true;
      setEditorAttempt((attempt) => attempt + 1);
      return;
    }
    wantsMonaco.current = simple;
    setSimple((value) => !value);
  }
  const [status, setStatus] = useState("Loading draft…");
  const key = `solver-ai:draft:v1:${slug}:${language}`;
  useEffect(() => {
    try {
      const stored = localStorage.getItem(key);
      setCode(stored ?? starter);
      onCodeChange?.(stored ?? starter);
      setStatus(
        stored === null
          ? "Starter code · not yet edited"
          : "Draft restored from this browser",
      );
    } catch {
      onCodeChange?.(starter);
      setStatus("Browser storage unavailable · copy your code to keep it");
    }
    setReady(true);
  }, [key, starter, onCodeChange]);
  function update(value: string | undefined) {
    if (!ready || value === undefined) return;
    setCode(value);
    onCodeChange?.(value);
    try {
      localStorage.setItem(key, value);
      setStatus("Saved in this browser");
    } catch {
      setStatus("Draft could not be saved · copy your code to keep it");
    }
  }
  function reset() {
    if (
      window.confirm(
        "Reset this language’s draft to starter code? Your saved code will be replaced.",
      )
    )
      update(starter);
  }
  return (
    <>
      <div className="editor-actions">
        <span>{language === "python" ? "main.py" : "main.cpp"}</span>
        <div>
          <button
            type="button"
            onClick={toggleEditor}
            disabled={simple && editorLoading}
          >
            {simple && editorError
              ? "Retry Monaco editor"
              : simple && editorLoading
                ? "Loading Monaco…"
                : simple
                  ? "Use Monaco editor"
                  : "Use simple editor"}
          </button>
          <button type="button" onClick={reset} disabled={!ready}>
            Reset draft
          </button>
        </div>
      </div>
      {editorError && (
        <p className="storage-note" role="alert">
          {editorError}. The simple editor is available; your draft is
          preserved. Use “Retry Monaco editor” to try again.
        </p>
      )}
      <div className="editor-surface">
        {!ready ? (
          <p role="status">Loading draft…</p>
        ) : simple ? (
          <textarea
            className="simple-editor"
            aria-label="Code editor"
            value={code}
            onChange={(e) => update(e.target.value)}
            spellCheck={false}
          />
        ) : !editorReady ? (
          <p role="status">
            Loading editor… You can also use the simple editor above.
          </p>
        ) : (
          <Editor
            height="460px"
            language={language}
            value={code}
            onChange={update}
            loading={
              <span role="status">
                Loading editor… You can also use the simple editor above.
              </span>
            }
            options={{
              minimap: { enabled: false },
              fontSize: 14,
              lineHeight: 23,
              padding: { top: 18 },
              scrollBeyondLastLine: false,
              automaticLayout: true,
              tabSize: 4,
              ariaLabel: "Code editor",
              wordWrap: "on",
            }}
          />
        )}
      </div>
      <div className="draft-status" role="status">
        {status}
      </div>
      <p className="storage-note">
        Drafts save in this browser, separately for each problem and language.
        Your code is sent for judging only when you choose Run or Submit.
      </p>
    </>
  );
}
