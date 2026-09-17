import React, { useEffect, useState } from "react";
import { api } from "../api/client";

const PANEL_SPEC = [
  { id: "audit_rate", title: "Audit events", hint: "total_events" },
  { id: "tool_errors", title: "Errors", hint: "error_count" },
  { id: "health", title: "Dependency health", hint: "health_snapshot" },
  { id: "dry_run_ratio", title: "Dry-run vs live", hint: "prefer dry_run until activation" },
];

export default function OpsPage() {
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState("");
  const grafanaUrl = typeof localStorage !== "undefined" ? localStorage.getItem("nivy_grafana_url") || "" : "";

  useEffect(() => {
    api.observabilitySummary().then(setSummary).catch((e) => setError(e.message || String(e)));
  }, []);

  const audit = summary?.audit || {};

  return (
    <div>
      <h2>Ops / Observability</h2>
      <p className="muted">OC-4.2 — Mirrors ops/observability/dashboard-spec.yaml. Grafana iframe optional.</p>
      {error && <div className="banner err">{error}</div>}
      <div className="grid">
        <div className="card"><div className="label">Audit events</div><div className="value">{audit.total_events ?? "—"}</div></div>
        <div className="card err"><div className="label">Errors</div><div className="value">{audit.error_count ?? "—"}</div></div>
        <div className="card warn"><div className="label">Approvals pending</div><div className="value">{summary?.approvals_pending ?? "—"}</div></div>
      </div>
      <div className="panel">
        <h3>Dashboard panels (spec)</h3>
        <ul className="panel-list">
          {PANEL_SPEC.map((p) => (
            <li key={p.id}><strong>{p.title}</strong><span className="muted"> — {p.hint}</span></li>
          ))}
        </ul>
        {grafanaUrl ? (
          <iframe title="Grafana" src={grafanaUrl} className="grafana-frame" />
        ) : (
          <p className="muted">Set localStorage.nivy_grafana_url to embed Grafana. Until then use cards + audit browser.</p>
        )}
      </div>
      {summary && <div className="panel"><h3>Raw summary</h3><pre className="json">{JSON.stringify(summary, null, 2)}</pre></div>}
    </div>
  );
}
