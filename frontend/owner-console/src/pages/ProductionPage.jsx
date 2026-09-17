import { useEffect, useState } from "react";

const STORAGE_KEY = "nivy_production_checklist";

const SECTIONS = [
  {
    id: "A",
    title: "A. Security",
    items: [
      "python3 scripts/check_no_secrets_in_git.py → OK",
      "CI quality-gates secret scan green on main",
      ".env not in Git; secrets in env/secret store",
      "Strong unique POSTGRES_PASSWORD and provider keys",
      "Protected tools require approval",
      "Audit redaction verified",
    ],
  },
  {
    id: "B",
    title: "B. Data durability",
    items: [
      "Postgres backup script succeeds",
      "Restore drill documented",
      "Backup retention set",
    ],
  },
  {
    id: "C",
    title: "C. Runtime / workflows",
    items: [
      "pytest backend/app/test_lead_skills.py green",
      "Lead-outreach dry-run E2E green",
      "Knowledge retrieval mock tests green",
      "Live email only after approval process is live",
      "Inbound + marketing workflows remain dry_run_default until signed",
    ],
  },
  {
    id: "D",
    title: "D. Observability",
    items: ["Audit events flowing", "Dashboard panels reviewed", "Alerts on tool errors / failed workflows"],
  },
  {
    id: "E",
    title: "E. Definition of Done",
    items: ["Implementation, integration, schemas, errors, persistence, security, observability, tests, docs, acceptance"],
  },
];

function loadChecks() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return JSON.parse(raw);
  } catch {
    /* ignore */
  }
  return {};
}

function saveChecks(checks) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(checks));
}

export default function ProductionPage() {
  const [checks, setChecks] = useState(loadChecks);

  useEffect(() => {
    saveChecks(checks);
  }, [checks]);

  const toggle = (key) => {
    setChecks((c) => ({ ...c, [key]: !c[key] }));
  };

  const total = SECTIONS.reduce((n, s) => n + s.items.length, 0);
  const done = Object.values(checks).filter(Boolean).length;
  const allDone = done >= total;

  return (
    <div>
      <h2>Production activation</h2>
      <p className="muted">
        Checklist from <code>ops/checklists/PRODUCTION-ACTIVATION.md</code>. Progress is stored in this browser only
        (localStorage). Activation without complete sign-off is out of policy.
      </p>
      <div className={`banner ${allDone ? "ok" : "warn"}`}>
        Progress: {done}/{total} {allDone ? "— ready for sign-off" : "— incomplete"}
      </div>
      {SECTIONS.map((sec) => (
        <div className="panel" key={sec.id}>
          <strong>{sec.title}</strong>
          {sec.items.map((label, i) => {
            const key = `${sec.id}.${i}`;
            return (
              <label key={key} className="checkbox-row">
                <input type="checkbox" checked={!!checks[key]} onChange={() => toggle(key)} />
                <span>{label}</span>
              </label>
            );
          })}
        </div>
      ))}
      <div className="panel">
        <strong>Sign-off (manual)</strong>
        <p className="muted">Engineering · Ops / Security · Product owner — record names/dates in the markdown checklist.</p>
      </div>
    </div>
  );
}
