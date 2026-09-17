import React, { useState } from "react";
const CHECKS = [
  { id: "https", label: "HTTPS termination" },
  { id: "auth", label: "Owner auth gate" },
  { id: "secrets", label: "Secrets not in Git" },
  { id: "dryrun", label: "Dry-run proven before live email" },
  { id: "approval", label: "Side effects require approval_id" },
  { id: "backup", label: "Backup/restore drill done" },
  { id: "cors", label: "CORS restricted in prod" },
  { id: "checklist", label: "PRODUCTION-ACTIVATION.md signed" },
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
  return (
    <div>
      <h2>Production deploy</h2>
      <p className="muted">OC-4.4 — Checklist before non-local use.</p>
      <div className="card"><div className="label">Progress</div><div className="value">{CHECKS.filter((c) => done[c.id]).length}/{CHECKS.length}</div></div>
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
