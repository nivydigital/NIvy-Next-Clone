const SETTINGS_KEY = "nivy_owner_console_settings";

export function loadSettings() {
  try {
    const raw = localStorage.getItem(SETTINGS_KEY);
    if (raw) return { baseUrl: "http://localhost:8000", dryRunDefault: true, ...JSON.parse(raw) };
  } catch {
    /* ignore */
  }
  return { baseUrl: "http://localhost:8000", dryRunDefault: true };
}

export function saveSettings(settings) {
  localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
}

async function request(path, options = {}) {
  const { baseUrl } = loadSettings();
  const url = `${baseUrl.replace(/\/$/, "")}${path}`;
  const res = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  });
  let data = null;
  const text = await res.text();
  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = { raw: text };
  }
  if (!res.ok) {
    const detail = data?.detail || data?.error || text || res.statusText;
    const err = new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
    err.status = res.status;
    err.data = data;
    throw err;
  }
  return data;
}

export const api = {
  health: () => request("/health"),
  runtimeHealth: () => request("/api/v1/runtime/health"),
  system: () => request("/api/v1/system"),
  evaluation: () => request("/api/v1/evaluation/runtime"),
  listAgents: () => request("/api/v1/runtime/agents"),
  getAgent: (id) => request(`/api/v1/runtime/agents/${id}`),
  resolveSkills: (id) => request(`/api/v1/runtime/agents/${id}/skills/resolve`),
  skillCoverage: () => request("/api/v1/runtime/skills/coverage"),
  executeAgent: (id, body) =>
    request(`/api/v1/runtime/agents/${id}/execute`, { method: "POST", body: JSON.stringify(body) }),
  runAgent: (id, body) =>
    request(`/api/v1/runtime/agents/${id}/run`, { method: "POST", body: JSON.stringify(body) }),
  runA001: (body) =>
    request("/api/v1/runtime/agents/A001/research", { method: "POST", body: JSON.stringify(body) }),
  listWorkflows: () => request("/api/v1/runtime/workflows"),
  getWorkflow: (id) => request(`/api/v1/runtime/workflows/${id}`),
  runWorkflow: (id, body) =>
    request(`/api/v1/runtime/workflows/${id}/run`, { method: "POST", body: JSON.stringify(body) }),
  listLeads: () => request("/api/v1/revenue/leads"),
  createLead: (body) =>
    request("/api/v1/revenue/leads", { method: "POST", body: JSON.stringify(body) }),
  qualifyLead: (id, score) =>
    request(`/api/v1/revenue/leads/${id}/qualify`, {
      method: "POST",
      body: JSON.stringify({ score }),
    }),
  revenueSummary: () => request("/api/v1/revenue/summary"),
  leadAudit: (id) => request(`/api/v1/revenue/leads/${id}/audit`),
  listApprovals: () => request("/api/v1/runtime/approvals"),
  requestApproval: (body) =>
    request("/api/v1/runtime/approvals", { method: "POST", body: JSON.stringify(body) }),
  approve: (id) => request(`/api/v1/runtime/approvals/${id}/approve`, { method: "POST" }),
  sendEmail: (body) =>
    request("/api/v1/email/send", { method: "POST", body: JSON.stringify(body) }),
};
