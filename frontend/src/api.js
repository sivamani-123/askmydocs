const token = () => localStorage.getItem("token");

async function call(path, options = {}) {
  const headers = { ...(options.headers || {}) };
  if (token()) headers.Authorization = `Bearer ${token()}`;
  const res = await fetch(path, { ...options, headers });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(typeof body.detail === "string" ? body.detail : "Request failed");
  }
  return res.status === 204 ? null : res.json();
}

const json = (body) => ({ method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });

export const api = {
  login: (b) => call("/api/auth/login", json(b)),
  register: (b) => call("/api/auth/register", json(b)),
  documents: () => call("/api/documents"),
  upload: (file) => { const f = new FormData(); f.append("file", file); return call("/api/documents", { method: "POST", body: f }); },
  remove: (id) => call(`/api/documents/${id}`, { method: "DELETE" }),
  ask: (question) => call("/api/chat/ask", json({ question })),
};
