import { useEffect, useState } from "react";
import { api } from "./api.js";

function Auth({ onDone }) {
  const [mode, setMode] = useState("login");
  const [form, setForm] = useState({ full_name: "", email: "", password: "" });
  const [error, setError] = useState("");
  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const out = mode === "login" ? await api.login(form) : await api.register(form);
      localStorage.setItem("token", out.access_token);
      localStorage.setItem("name", out.full_name);
      onDone();
    } catch (err) { setError(err.message); }
  };

  return (
    <main className="auth">
      <h1>AskMyDocs</h1>
      <p className="lead">Ask questions across your own documents and get answers with sources.</p>
      <form onSubmit={submit}>
        {mode === "register" && <input placeholder="Full name" value={form.full_name} onChange={set("full_name")} required />}
        <input type="email" placeholder="Email" value={form.email} onChange={set("email")} required />
        <input type="password" placeholder="Password (8+ characters)" value={form.password} onChange={set("password")} required minLength={8} />
        {error && <p className="error" role="alert">{error}</p>}
        <button>{mode === "login" ? "Sign in" : "Create account"}</button>
      </form>
      <button className="link" onClick={() => setMode(mode === "login" ? "register" : "login")}>
        {mode === "login" ? "Create an account" : "I already have an account"}
      </button>
    </main>
  );
}

function Workspace({ onLogout }) {
  const [docs, setDocs] = useState([]);
  const [question, setQuestion] = useState("");
  const [thread, setThread] = useState([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const load = () => api.documents().then(setDocs).catch((e) => setError(e.message));
  useEffect(() => { load(); }, []);

  const upload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setBusy(true); setError("");
    try { await api.upload(file); await load(); } catch (err) { setError(err.message); }
    setBusy(false); e.target.value = "";
  };

  const ask = async (e) => {
    e.preventDefault();
    const q = question.trim();
    if (!q) return;
    setQuestion(""); setBusy(true); setError("");
    try { const out = await api.ask(q); setThread((t) => [...t, { q, ...out }]); }
    catch (err) { setError(err.message); }
    setBusy(false);
  };

  return (
    <div className="shell">
      <aside>
        <h2>Documents</h2>
        <label className="upload">
          {busy ? "Working…" : "Upload PDF or text"}
          <input type="file" accept=".pdf,.txt,.md" onChange={upload} disabled={busy} hidden />
        </label>
        <ul>
          {docs.map((d) => (
            <li key={d.id}>
              <strong>{d.filename}</strong>
              <span>{d.category} · {d.num_chunks} passages</span>
              <button className="link" onClick={() => api.remove(d.id).then(load)}>Delete</button>
            </li>
          ))}
          {!docs.length && <li className="empty">Upload your first document to start asking questions.</li>}
        </ul>
        <button className="link" onClick={onLogout}>Sign out ({localStorage.getItem("name")})</button>
      </aside>
      <main>
        <div className="thread">
          {thread.map((m, i) => (
            <article key={i}>
              <p className="q">{m.q}</p>
              <p className="a">{m.answer}</p>
              <details>
                <summary>{m.sources.length} sources · {m.mode === "llm" ? "LLM answer" : "extractive answer"}</summary>
                {m.sources.map((s, j) => (
                  <blockquote key={j}><b>{s.filename}</b> (match {s.score})<br />{s.snippet}…</blockquote>
                ))}
              </details>
            </article>
          ))}
          {!thread.length && <p className="empty">Ask something about your documents.</p>}
        </div>
        {error && <p className="error" role="alert">{error}</p>}
        <form className="ask" onSubmit={ask}>
          <input value={question} onChange={(e) => setQuestion(e.target.value)} placeholder="What does the contract say about termination?" />
          <button disabled={busy}>Ask</button>
        </form>
      </main>
    </div>
  );
}

export default function App() {
  const [authed, setAuthed] = useState(!!localStorage.getItem("token"));
  return authed
    ? <Workspace onLogout={() => { localStorage.clear(); setAuthed(false); }} />
    : <Auth onDone={() => setAuthed(true)} />;
}
