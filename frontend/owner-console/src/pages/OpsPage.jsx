import React, { useEffect, useState } from "react";
import { api } from "../api/client";

export default function OpsPage() {
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState("");
  useEffect(() => {
    api.observabilitySummary().then(setSummary).catch((e) => setError(e.message || String(e)));
  }, []);
  const audit = summary?.audit || {};
  return (
    <div>
      <h2>Ops / Observability</h2>
      <p className="muted">OC-4.2 — dashboard-spec panels as cards; Grafana iframe optional via localStorage.nivy_grafana_url.</p>
      {error && <div className="banner err">{error}</div>}
      <div className="grid">
        <div className="card"><div className="label">Audit events</div><div className="value">{audit.total_events ?? "—"}</div></div>
        <div className="card err"><div className="label">Errors</div><div className="value">{audit.error_count ?? "—"}</div></div>
        <div className="card warn"><div className="label">Approvals pending</div><div className="value">{summary?.approvals_pending ?? "—"}</div></div>
      </div>
      {summary && <div className="panel"><pre className="json">{JSON.stringify(summary, null, 2)}</pre></div>}
    </div>
  );
}
