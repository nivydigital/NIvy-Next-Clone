import React from "react";
export default function RolesPage() {
  return (
    <div>
      <h2>Roles & access</h2>
      <p className="muted">OC-4.3 — Multi-user RBAC deferred. MVP = single company owner.</p>
      <div className="panel">
        <table>
          <thead><tr><th>Role</th><th>Access</th><th>Status</th></tr></thead>
          <tbody>
            <tr><td>Company owner</td><td>Full console</td><td>MVP</td></tr>
            <tr><td>Operator</td><td>—</td><td>Deferred</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
