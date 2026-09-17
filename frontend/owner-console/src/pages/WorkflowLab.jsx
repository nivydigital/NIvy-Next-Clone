import { useEffect, useState } from "react";
import { api, loadSettings } from "../api/client.js";
import { WORKFLOW_PRESETS } from "../presets.js";

function extractWorkflowIds(data) {
  if (!data) return [];
  const items = data.items || data.workflows || data;
  if (!Array.isArray(items)) return [];
  return items.map((w) => w.id || w.workflow_id || w).filter(Boolean);
}

export default function WorkflowLab() {
  const settings = loadSettings();
  const [workflows, setWorkflows] = useState([]);
  const [workflowId, setWorkflowId] = useState("lead-outreach");
  const [dryRun, setDryRun] = useState(settings.dryRunDefault !== false);
  const [stopAfter, setStopAfter] = useState("");
  const [payloadText, setPayloadText] = useState(
    JSON.stringify(WORKFLOW_PRESETS["lead-outreach"].payload, null, 2)
  );
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [busy, setBusy] = useState(false);
  const [loadError, setLoadError] = useState(null);

  useEffect(() => {
    api
      .listWorkflows()
      .then((data) => {
        const ids = extractWorkflowIds(data);
        setWorkflows(
          ids.length
            ? ids
            : ["lead-outreach", "inbound-email-triage", "content-calendar", "social-content-pipeline"]
        );
      })
      .catch((e) => {
        setLoadError(e.message);
        setWorkflows(["lead-outreach", "inbound-email-triage", "content-calendar", "seo-audit"]);
      });
  }, []);

  function applyPreset() {
    const p = WORKFLOW_PRESETS[workflowId];
    if (p) setPayloadText(JSON.stringify(p.payload, null, 2));
  }

  async function run() {
    if (!dryRun) {
      const ok = window.confirm("Dry-run is OFF. This may allow side effects. Continue?");
      if (!ok) return;
    }
    setBusy(true);
    setError(null);
    setResult(null);
    try {
      const payload = JSON.parse(payloadText);
      const body = {
        payload,
        dry_run: dryRun,
      };
      if (stopAfter.trim()) body.stop_after_stage = stopAfter.trim();
      const data = await api.runWorkflow(workflowId, body);
      setResult(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div>
      <h2>Workflow Test Lab</h2>
      <p className="muted">Run workflows with dry-run default ON. Safe path for owner testing.</p>
      {loadError && <div className="banner warn">Workflow list API: {loadError}. Using fallback IDs.</div>}
      {!dryRun && <div className="banner warn">Dry-run is OFF — live side effects may run if backend allows.</div>}

      <div className="panel">
        <div className="row">
          <div>
            <label>Workflow</label>
            <select value={workflowId} onChange={(e) => setWorkflowId(e.target.value)}>
              {workflows.map((id) => (
                <option key={id} value={id}>
                  {id}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label>Stop after stage (optional)</label>
            <input value={stopAfter} onChange={(e) => setStopAfter(e.target.value)} placeholder="e.g. discover" />
          </div>
        </div>

        <div className="checkbox-row">
          <input id="dry" type="checkbox" checked={dryRun} onChange={(e) => setDryRun(e.target.checked)} />
          <label htmlFor="dry" style={{ margin: 0 }}>
            Dry-run
          </label>
        </div>

        <label>Payload (JSON)</label>
        <textarea value={payloadText} onChange={(e) => setPayloadText(e.target.value)} />

        <button type="button" className="secondary" onClick={applyPreset}>
          Load preset
        </button>
        <button type="button" disabled={busy} onClick={run}>
          Run workflow
        </button>
      </div>

      {error && <div className="banner err">{error}</div>}
      {result && (
        <div className="panel">
          <strong>Result</strong>
          <pre className="result">{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
      {busy && <p className="muted">Running…</p>}
    </div>
  );
}
