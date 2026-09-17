import React, { useState } from "react";

const CHECKS = [
  { id: "https", label: "HTTPS termination (reverse proxy / cloud LB)" },
  { id: "auth", label: "Owner auth gate (OWNER_CONSOLE_PASSWORD or IdP)" },
  { id: "secrets", label: "Secrets only in env/secret store" },
  { id: "dryrun", label: "LEAD_OUTREACH_DRY_RUN proven before live email" },
  { id: "approval", label: "Email/CRM side effects require approval_id" },
  { id: "backup", label: "Postgres backup/restore drill recorded" },
  { id: "cors", label: "CORS restricted to console origin in prod" },
  { id: "checklist", label: "ops/checklists/PRODUCTION-ACTIVATION.md signed" },
];

export default function ProductionPage() {
  const [done, setDone] = useState(() => {
    try { return JSON.parse(localStorage.getItem("nivy_prod_checks") || "{}"); } catch { return {}; }
  });

  function toggle(id) {
    const next = { ...done, [id]: !done[id] };
    setDone(next);
    localStorage.setItem("nivy_prod_checks", JSON.stringify(next));
  }

  const complete = CHECKS.filter((c) => done[c.id]).length;

  return (
    <div>
      <h2>Production deploy</h2>
      <p className="muted">OC-4.4 — Checklist before non-local use (STD-08 / activation checklist).</p>
      <div className="card"><div className="label">Progress</div><div className="value">{complete}/{CHECKS.length}</div></div>
      <div className="panel">
        <ul className="checklist">
          {CHECKS.map((c) => (
            <li key={c.id}><label><input type="checkbox" checked={!!done[c.id]} onChange={() => toggle(c.id)} /> {c.label}</label></li>
          ))}
        </ul>
      </div>
    </div>
  );
}
