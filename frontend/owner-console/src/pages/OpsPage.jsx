import { useEffect, useState } from "react";
import { api, loadSettings } from "../api/client.js";

function Card({ label, value, tone }) {
  return (
    <div className={`card ${tone || ""}`}>
      <div className="label">{label}</div>
      <div className="value">{value}</div>
    </div>
  );
}

export default function OpsPage() {
  const [state, setState] = useState({ loading: true, error: null, data: null });
  const [grafanaUrl, setGrafanaUrl] = useState(() => {
    try {
      return loadSettings().grafanaUrl || "";
    } catch {
      return "";
    }
  });

  const load = async () => {
    setState((s) => ({ ...s, loading: true, error: null }));
    try {
      const data = await api.observabilitySummary();
      setState({ loading: false, error: null, data });
    } catch (e) {
      setState({ loading: false, error: e.message, data: null });
    }
  };

  useEffect(() => {
    load();
  }, []);

  const { loading, error, data } = state;

  return (
    <div>
      <h2>Ops / Observability</h2>
      <p className="muted">
        MVP metrics from runtime audit. Full Grafana panels live in{" "}
        <code>ops/observability/dashboard-spec.yaml</code>.
      </p>
      <button type="button" className="secondary" onClick={load} disabled={loading}>
        {loading ? "Loading…" : "Refresh"}
      </button>
      {error && <div className="banner err">{error}</div>}
      {data && (
        <>
          <div className="grid" style={{ marginTop: 16 }}>
            <Card label="Audit events" value={data.audit_events ?? 0} />
            <Card label="Errors / denied" value={data.errors ?? 0} tone={data.errors > 0 ? "warn" : "ok"} />
            <Card label="Pending approvals" value={data.pending_approvals ?? 0} />
            <Card
              label="Runtime"
              value={data.runtime_health?.status || "—"}
              tone={data.runtime_health?.status === "ok" ? "ok" : "warn"}
            />
          </div>
          <div className="panel">
            <strong>By status</strong>
            <pre className="result">{JSON.stringify(data.by_status || {}, null, 2)}</pre>
          </div>
          <div className="panel">
            <strong>By event type</strong>
            <pre className="result">{JSON.stringify(data.by_event_type || {}, null, 2)}</pre>
          </div>
          {data.note && <p className="muted">{data.note}</p>}
        </>
      )}
      <div className="panel">
        <strong>Optional Grafana embed</strong>
        <label>Grafana dashboard URL (stored in settings)</label>
        <input
          value={grafanaUrl}
          onChange={(e) => setGrafanaUrl(e.target.value)}
          placeholder="https://grafana.example/d/nivy-ops"
        />
        {grafanaUrl ? (
          <iframe
            title="Grafana"
            src={grafanaUrl}
            style={{ width: "100%", height: 420, marginTop: 12, border: "1px solid var(--border)", borderRadius: 8 }}
          />
        ) : (
          <p className="muted">Paste a Grafana URL above to embed (optional).</p>
        )}
      </div>
    </div>
  );
}
