import React, { useEffect, useState } from "react";
import { api } from "../api/client";

export default function HistoryPage() {
  const [items, setItems] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [eventType, setEventType] = useState("");
  const [status, setStatus] = useState("");
  const [selected, setSelected] = useState(null);

  async function load() {
    setLoading(true);
    setError("");
    try {
      const data = await api.listAudit({ limit: 150, event_type: eventType || undefined, status: status || undefined });
      setItems(data.items || []);
    } catch (e) {
      setError(e.message || String(e));
      setItems([]);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { load(); }, []);

  return (
    <div>
      <h2>Run history / Audit</h2>
      <p className="muted">OC-4.1 — Runtime audit browser.</p>
      <div className="toolbar">
        <input placeholder="event_type" value={eventType} onChange={(e) => setEventType(e.target.value)} />
        <input placeholder="status" value={status} onChange={(e) => setStatus(e.target.value)} />
        <button type="button" onClick={load} disabled={loading}>{loading ? "Loading…" : "Refresh"}</button>
      </div>
      {error && <div className="banner err">{error}</div>}
      <div className="split">
        <div className="panel table-wrap">
          <table>
            <thead><tr><th>Time</th><th>Type</th><th>Action</th><th>Status</th></tr></thead>
            <tbody>
              {items.map((ev, i) => (
                <tr key={ev.event_id || i} onClick={() => setSelected(ev)} className={selected === ev ? "selected" : ""}>
                  <td className="mono">{(ev.timestamp || "").slice(0, 19)}</td>
                  <td>{ev.event_type}</td>
                  <td>{ev.action}</td>
                  <td>{ev.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="panel">
          <h3>Detail</h3>
          {selected ? <pre className="json">{JSON.stringify(selected, null, 2)}</pre> : <p className="muted">Select a row</p>}
        </div>
      </div>
    </div>
  );
}
