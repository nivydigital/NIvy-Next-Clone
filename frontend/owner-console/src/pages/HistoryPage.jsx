import { useEffect, useState } from "react";
import { api } from "../api/client.js";

export default function HistoryPage() {
  const [state, setState] = useState({ loading: true, error: null, items: [], selected: null });

  const load = async () => {
    setState((s) => ({ ...s, loading: true, error: null }));
    try {
      const data = await api.listAudit(200);
      setState({ loading: false, error: null, items: data.items || [], selected: null });
    } catch (e) {
      setState({ loading: false, error: e.message, items: [], selected: null });
    }
  };

  useEffect(() => {
    load();
  }, []);

  const { loading, error, items, selected } = state;

  return (
    <div>
      <h2>Run history / Audit</h2>
      <p className="muted">In-memory audit events from runtime (newest first). Refresh after agent/workflow runs.</p>
      <button type="button" className="secondary" onClick={load} disabled={loading}>
        {loading ? "Loading…" : "Refresh"}
      </button>
      {error && <div className="banner err">{error}</div>}
      {!loading && !error && items.length === 0 && (
        <div className="banner warn">No audit events yet. Run an agent or workflow, then refresh.</div>
      )}
      {items.length > 0 && (
        <div className="panel" style={{ marginTop: 16 }}>
          <table>
            <thead>
              <tr>
                <th>Time</th>
                <th>Type</th>
                <th>Action</th>
                <th>Status</th>
                <th>Actor</th>
              </tr>
            </thead>
            <tbody>
              {items.map((ev, i) => (
                <tr
                  key={ev.event_id || ev.request_id || i}
                  style={{ cursor: "pointer", background: selected === ev ? "#243044" : undefined }}
                  onClick={() => setState((s) => ({ ...s, selected: ev }))}
                >
                  <td>{(ev.timestamp || "—").slice(0, 19)}</td>
                  <td>{ev.event_type || "—"}</td>
                  <td>{ev.action || "—"}</td>
                  <td>{ev.status || "—"}</td>
                  <td>{ev.actor || "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      {selected && (
        <div className="panel">
          <strong>Event detail</strong>
          <pre className="result">{JSON.stringify(selected, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
