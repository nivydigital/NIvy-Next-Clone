import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api/client.js";

function Card({ label, value, tone }) {
  return (
    <div className={`card ${tone || ""}`}>
      <div className="label">{label}</div>
      <div className="value">{value}</div>
    </div>
  );
}

export default function Dashboard() {
  const [state, setState] = useState({ loading: true, error: null, data: {} });

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const [health, runtime, system, agents, workflows, revenue, evaluation, coverage] = await Promise.allSettled([
          api.health(),
          api.runtimeHealth(),
          api.system(),
          api.listAgents(),
          api.listWorkflows(),
          api.revenueSummary(),
          api.evaluation(),
          api.skillCoverage(),
        ]);
        if (cancelled) return;
        setState({
          loading: false,
          error: null,
          data: {
            health: health.status === "fulfilled" ? health.value : null,
            runtime: runtime.status === "fulfilled" ? runtime.value : null,
            system: system.status === "fulfilled" ? system.value : null,
            agents: agents.status === "fulfilled" ? agents.value : null,
            workflows: workflows.status === "fulfilled" ? workflows.value : null,
            revenue: revenue.status === "fulfilled" ? revenue.value : null,
            evaluation: evaluation.status === "fulfilled" ? evaluation.value : null,
            coverage: coverage.status === "fulfilled" ? coverage.value : null,
            offline: health.status === "rejected",
          },
        });
      } catch (e) {
        if (!cancelled) setState({ loading: false, error: e.message, data: {} });
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  const { loading, error, data } = state;
  if (loading) return <p className="muted">Loading dashboard…</p>;
  if (error) return <div className="banner err">{error}</div>;

  const agentCount = data.agents?.count ?? data.agents?.items?.length ?? "—";
  const wfCount = data.workflows?.items?.length ?? "—";
  const leads = data.revenue?.total_leads ?? "—";
  const evalPass = data.evaluation ? `${data.evaluation.passed}/${data.evaluation.total}` : "—";

  return (
    <div>
      <h2>Dashboard</h2>
      <p className="muted">System health and quick counts for the company owner.</p>
      {data.offline && <div className="banner err">Backend unreachable. Start API on the URL in Settings.</div>}
      <div className="grid">
        <Card label="Backend" value={data.health?.status || "down"} tone={data.health?.status === "ok" ? "ok" : "err"} />
        <Card label="Runtime" value={data.runtime?.status || data.system?.status || "—"} tone={data.runtime?.status === "ok" || data.system?.status === "online" ? "ok" : "warn"} />
        <Card label="Agents" value={agentCount} />
        <Card label="Workflows" value={wfCount} />
        <Card label="Leads" value={leads} />
        <Card label="Eval checks" value={evalPass} />
      </div>

      <div className="panel">
        <strong>System</strong>
        <pre className="result">{JSON.stringify(data.system || data.health || {}, null, 2)}</pre>
      </div>

      {data.revenue?.by_status && (
        <div className="panel">
          <strong>Leads by status</strong>
          <pre className="result">{JSON.stringify(data.revenue.by_status, null, 2)}</pre>
        </div>
      )}

      {data.coverage && (
        <div className="panel">
          <strong>Skill coverage (snapshot)</strong>
          <pre className="result">{JSON.stringify(data.coverage, null, 2)}</pre>
        </div>
      )}

      <div className="panel">
        <strong>Quick links</strong>
        <p className="muted">
          <Link to="/test/agents">Test an agent</Link> · <Link to="/test/workflows">Run workflow dry-run</Link> ·{" "}
          <Link to="/leads">Manage leads</Link> · <Link to="/approvals">Approvals</Link>
        </p>
      </div>
    </div>
  );
}
