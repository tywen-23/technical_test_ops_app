const BASE = import.meta.env.VITE_API_URL || "http://localhost:8010";

function qs(obj) {
  const p = new URLSearchParams();
  Object.entries(obj || {}).forEach(([k, v]) => {
    if (v) p.set(k, v);
  });
  const s = p.toString();
  return s ? `?${s}` : "";
}

async function request(path, opts) {
  const res = await fetch(BASE + path, opts);
  if (!res.ok) {
    const text = await res.text().catch(() => res.statusText);
    throw new Error(text || `HTTP ${res.status}`);
  }
  return res.json();
}

export const getSummary = (q) => request(`/api/summary${qs(q)}`);
export const getSales = (q) => request(`/api/sales${qs(q)}`);
export const getFilters = () => request(`/api/filters`);

export const getPace = (month) =>
  request(`/api/pace${qs({month})}`);

export const createSale = (body) =>
  request(`/api/sales`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

export const deleteSale = (id) => request(`/api/sales/${id}`, { method: "DELETE" });
