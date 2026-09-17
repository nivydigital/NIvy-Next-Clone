import { useEffect, useState } from "react";
import { api } from "../api/client.js";
import { AGENT_PRESETS } from "../presets.js";

function extractAgentIds(data) {
  if (!data) return [];
  if (Array.isArray(data.items)) {
    return data.items.map((a) => a.id || a.agent_id || a).filter(Boolean);
  }
  if (Array.isArray(data.agents)) {
    return data.agents.map((a) => a.id || a.agent_id || a).filter(Boolean);
  }
  if (Array.isArray(data)) return data.map((a) => a.id || a).filter(Boolean);
  return [];
}

export default function AgentLab() {
  const [agents, setAgents] = useState([]);
  const [agentId, setAgentId] = useState("A034");
  const [payloadText, setPayloadText] = useState(JSON.stringify(AGENT_PRESETS.A034.payload, null, 2));
  const [prompt, setPrompt] = useState("Summarize ICP fit for B2B automation buyers in India.");
  const [skills, setSkills] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [busy, setBusy] = useState(false);
  const [loadError, setLoadError] = useState(null);

  useEffect(() => {
    api
      .listAgents()
      .then((data) => {
        const ids = extractAgentIds(data);
        setAgents(ids.length ? ids : ["A001", "A034", "A044"]);
        if (ids.length && !ids.includes(agentId)) setAgentId(ids[0]);
      })
      .catch((e) => {
        setLoadError(e.message);
        setAgents(["A001", "A034", "A044", "A002", "A003"]);
      });
  }, []);

  async function loadSkills() {
    setError(null);
    try {
      const data = await api.resolveSkills(agentId);
      setSkills(data);
    } catch (e) {
      setSkills(null);
      setError(e.message);
    }
  }

  function applyPreset() {
    const p = AGENT_PRESETS[agentId];
    if (p) setPayloadText(JSON.stringify(p.payload, null, 2));
  }

  async function runExecute() {
    setBusy(true);
    setError(null);
    setResult(null);
    try {
      const payload = JSON.parse(payloadText);
      if (agentId === "A001" && payload.research_question) {
        const data = await api.runA001(payload);
        setResult(data);
      } else {
        const data = await api.executeAgent(agentId, { payload, allow_llm_fallback: true });
        setResult(data);
      }
    } catch (e) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  }

  async function runLlm() {
    setBusy(true);
    setError(null);
    setResult(null);
    try {
      let context = {};
      try {
        context = JSON.parse(payloadText);
      } catch {
        context = {};
      }
      const data = await api.runAgent(agentId, { prompt, context });
      setResult(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div>
      <h2>Agent Test Lab</h2>
      <p className="muted">Pick an agent, edit payload, run execute or LLM. No curl needed.</p>
      {loadError && <div className="banner warn">Agent list API: {loadError}. Using fallback IDs.</div>}

      <div className="panel">
        <div className="row">
          <div>
            <label>Agent</label>
            <select value={agentId} onChange={(e) => setAgentId(e.target.value)}>
              {agents.map((id) => (
                <option key={id} value={id}>
                  {id}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label>&nbsp;</label>
            <button type="button" className="secondary" onClick={applyPreset}>
              Load preset
            </button>
            <button type="button" className="secondary" onClick={loadSkills}>
              Resolve skills
            </button>
          </div>
        </div>

        <label>Payload (JSON)</label>
        <textarea value={payloadText} onChange={(e) => setPayloadText(e.target.value)} />

        <label>Prompt (for Run LLM)</label>
        <input value={prompt} onChange={(e) => setPrompt(e.target.value)} />

        <button type="button" disabled={busy} onClick={runExecute}>
          Execute
        </button>
        <button type="button" className="secondary" disabled={busy} onClick={runLlm}>
          Run LLM
        </button>
      </div>

      {skills && (
        <div className="panel">
          <strong>Skills resolve</strong>
          <pre className="result">{JSON.stringify(skills, null, 2)}</pre>
        </div>
      )}

      {error && <div className="banner err">{error}</div>}
      {result && (
        <div className="panel">
          <strong>Result</strong>
          <pre className="result">{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
      {!result && !error && !busy && <p className="muted">Run a test to see output here.</p>}
      {busy && <p className="muted">Running…</p>}
    </div>
  );
}
