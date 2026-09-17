import { useState } from "react";
import { loadSettings, saveSettings } from "../api/client.js";

export default function Settings() {
  const [form, setForm] = useState(loadSettings());
  const [saved, setSaved] = useState(false);

  function onSave(e) {
    e.preventDefault();
    saveSettings(form);
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  }

  return (
    <div>
      <h2>Settings</h2>
      <p className="muted">Stored in this browser only (localStorage).</p>
      <div className="panel">
        <form onSubmit={onSave}>
          <label>API base URL</label>
          <input
            value={form.baseUrl}
            onChange={(e) => setForm({ ...form, baseUrl: e.target.value })}
            placeholder="http://localhost:8000"
          />
          <div className="checkbox-row">
            <input
              id="dryDefault"
              type="checkbox"
              checked={form.dryRunDefault !== false}
              onChange={(e) => setForm({ ...form, dryRunDefault: e.target.checked })}
            />
            <label htmlFor="dryDefault" style={{ margin: 0 }}>
              Workflow dry-run default ON
            </label>
          </div>
          <button type="submit">Save</button>
          {saved && <span className="muted"> Saved.</span>}
        </form>
      </div>
      <div className="panel">
        <strong>Docs</strong>
        <ul className="muted">
          <li>Owner Console plan: docs/owner-console/IMPLEMENTATION-PLAN.md</li>
          <li>Progress: docs/owner-console/PROGRESS-TRACKER.md</li>
          <li>Production activation: ops/checklists/PRODUCTION-ACTIVATION.md</li>
        </ul>
      </div>
    </div>
  );
}
