import { useEffect, useState } from "react";
import { api } from "../api/client.js";

export default function Approvals() {
  const [items, setItems] = useState([]);
  const [error, setError] = useState(null);
  const [info, setInfo] = useState(null);
  const [form, setForm] = useState({ agent_id: "A044", tool_id: "tool.email.send", reason: "Owner console test" });
  const [approvalId, setApprovalId] = useState("");
  const [email, setEmail] = useState({
    to: "",
    subject: "Test from Owner Console",
    body: "<p>Hello from Nivy Owner Console (gated send).</p>",
    approval_id: "",
  });

  async function refresh() {
    setError(null);
    try {
      const data = await api.listApprovals();
      setItems(data.items || data || []);
    } catch (e) {
      setItems([]);
      setInfo(`Approvals list not available (${e.message}). You can still request + approve by ID.`);
    }
  }

  useEffect(() => {
    refresh();
  }, []);

  async function requestApproval(e) {
    e.preventDefault();
    setError(null);
    setInfo(null);
    try {
      const data = await api.requestApproval(form);
      const id = data.approval_id || data.id || data.approval?.approval_id;
      if (id) {
        setApprovalId(id);
        setEmail((prev) => ({ ...prev, approval_id: id }));
      }
      setInfo(JSON.stringify(data, null, 2));
      await refresh();
    } catch (err) {
      setError(err.message);
    }
  }

  async function approve() {
    if (!approvalId) return;
    setError(null);
    try {
      const data = await api.approve(approvalId);
      setInfo(JSON.stringify(data, null, 2));
      await refresh();
    } catch (err) {
      setError(err.message);
    }
  }

  async function sendEmail(e) {
    e.preventDefault();
    setError(null);
    try {
      const data = await api.sendEmail({
        to: email.to,
        subject: email.subject,
        body: email.body,
        body_type: "text/html",
        approval_id: email.approval_id || null,
        verify_email: true,
        send_after_verification: true,
      });
      setInfo(JSON.stringify(data, null, 2));
      if (data.approval?.approval_id) {
        setApprovalId(data.approval.approval_id);
        setEmail((prev) => ({ ...prev, approval_id: data.approval.approval_id }));
      }
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div>
      <h2>Approvals</h2>
      <p className="muted">Request approval, approve by ID, then optionally send email with approval_id.</p>
      {error && <div className="banner err">{error}</div>}

      <div className="panel">
        <strong>Request approval</strong>
        <form onSubmit={requestApproval}>
          <div className="row">
            <div>
              <label>Agent ID</label>
              <input value={form.agent_id} onChange={(e) => setForm({ ...form, agent_id: e.target.value })} />
            </div>
            <div>
              <label>Tool ID</label>
              <input value={form.tool_id} onChange={(e) => setForm({ ...form, tool_id: e.target.value })} />
            </div>
          </div>
          <label>Reason</label>
          <input value={form.reason} onChange={(e) => setForm({ ...form, reason: e.target.value })} />
          <button type="submit">Request</button>
        </form>
      </div>

      <div className="panel">
        <strong>Approve</strong>
        <label>Approval ID</label>
        <input value={approvalId} onChange={(e) => setApprovalId(e.target.value)} />
        <button type="button" onClick={approve}>
          Approve
        </button>
        <button type="button" className="secondary" onClick={refresh}>
          Refresh list
        </button>
      </div>

      {items?.length > 0 && (
        <div className="panel">
          <strong>Pending / known approvals</strong>
          <pre className="result">{JSON.stringify(items, null, 2)}</pre>
        </div>
      )}

      <div className="panel">
        <strong>Email send (gated)</strong>
        <form onSubmit={sendEmail}>
          <label>To</label>
          <input type="email" required value={email.to} onChange={(e) => setEmail({ ...email, to: e.target.value })} />
          <label>Subject</label>
          <input value={email.subject} onChange={(e) => setEmail({ ...email, subject: e.target.value })} />
          <label>Body</label>
          <textarea value={email.body} onChange={(e) => setEmail({ ...email, body: e.target.value })} />
          <label>Approval ID</label>
          <input value={email.approval_id} onChange={(e) => setEmail({ ...email, approval_id: e.target.value })} />
          <button type="submit">Send email</button>
        </form>
      </div>

      {info && (
        <div className="panel">
          <strong>Last response</strong>
          <pre className="result">{info}</pre>
        </div>
      )}
    </div>
  );
}
