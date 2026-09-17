import { useEffect, useState } from "react";
import { api } from "../api/client.js";

export default function Leads() {
  const [items, setItems] = useState([]);
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState(null);
  const [form, setForm] = useState({ name: "", email: "", company: "", source: "owner-console" });
  const [qualifyId, setQualifyId] = useState("");
  const [score, setScore] = useState(70);
  const [audit, setAudit] = useState(null);

  async function refresh() {
    setError(null);
    try {
      const [leads, sum] = await Promise.all([api.listLeads(), api.revenueSummary()]);
      setItems(leads.items || leads || []);
      setSummary(sum);
    } catch (e) {
      setError(e.message);
    }
  }

  useEffect(() => {
    refresh();
  }, []);

  async function createLead(e) {
    e.preventDefault();
    setError(null);
    try {
      await api.createLead({ ...form, actor: "owner" });
      setForm({ name: "", email: "", company: "", source: "owner-console" });
      await refresh();
    } catch (err) {
      setError(err.message);
    }
  }

  async function qualify() {
    if (!qualifyId) return;
    setError(null);
    try {
      await api.qualifyLead(qualifyId, Number(score));
      await refresh();
    } catch (err) {
      setError(err.message);
    }
  }

  async function showAudit(id) {
    setError(null);
    try {
      const data = await api.leadAudit(id);
      setAudit(data);
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div>
      <h2>Leads</h2>
      <p className="muted">Create and qualify leads via the revenue API.</p>
      {error && <div className="banner err">{error}</div>}

      {summary && (
        <div className="grid">
          <div className="card">
            <div className="label">Total leads</div>
            <div className="value">{summary.total_leads ?? "—"}</div>
          </div>
        </div>
      )}

      <div className="panel">
        <strong>Create lead</strong>
        <form onSubmit={createLead}>
          <div className="row">
            <div>
              <label>Name</label>
              <input required value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
            </div>
            <div>
              <label>Email</label>
              <input required type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
            </div>
            <div>
              <label>Company</label>
              <input value={form.company} onChange={(e) => setForm({ ...form, company: e.target.value })} />
            </div>
          </div>
          <button type="submit">Create</button>
        </form>
      </div>

      <div className="panel">
        <strong>Qualify</strong>
        <div className="row">
          <div>
            <label>Lead ID</label>
            <input value={qualifyId} onChange={(e) => setQualifyId(e.target.value)} placeholder="lead id" />
          </div>
          <div>
            <label>Score</label>
            <input type="number" value={score} onChange={(e) => setScore(e.target.value)} />
          </div>
        </div>
        <button type="button" onClick={qualify}>
          Qualify
        </button>
      </div>

      <div className="panel">
        <strong>Leads list</strong>
        <button type="button" className="secondary" onClick={refresh}>
          Refresh
        </button>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Status</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {(items || []).map((lead) => (
              <tr key={lead.id || lead.email}>
                <td>{lead.id}</td>
                <td>{lead.name}</td>
                <td>{lead.email}</td>
                <td>{lead.status}</td>
                <td>
                  <button type="button" className="secondary" onClick={() => { setQualifyId(lead.id); showAudit(lead.id); }}>
                    Audit
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {!items?.length && <p className="muted">No leads yet.</p>}
      </div>

      {audit && (
        <div className="panel">
          <strong>Audit</strong>
          <pre className="result">{JSON.stringify(audit, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
