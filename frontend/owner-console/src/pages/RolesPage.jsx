import React from "react";

export default function RolesPage() {
  return (
    <div>
      <h2>Roles & access</h2>
      <p className="muted">OC-4.3 — Multi-user RBAC is out of MVP scope.</p>
      <div className="panel">
        <table>
          <thead><tr><th>Role</th><th>Access</th><th>Status</th></tr></thead>
          <tbody>
            <tr><td>Company owner</td><td>Full Owner Console</td><td>MVP target</td></tr>
            <tr><td>Operator</td><td>Not in MVP</td><td>Deferred</td></tr>
            <tr><td>Customer</td><td>N/A</td><td>Out of scope</td></tr>
          </tbody>
        </table>
        <p className="muted" style={{ marginTop: 12 }}>
          Before multi-user: password gate (Phase 3) and production HTTPS auth (OC-4.4).
        </p>
      </div>
    </div>
  );
}
