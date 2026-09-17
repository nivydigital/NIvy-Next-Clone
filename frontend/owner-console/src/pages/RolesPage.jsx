export default function RolesPage() {
  return (
    <div>
      <h2>Roles / Multi-user</h2>
      <div className="banner warn">Deferred — out of MVP scope.</div>
      <div className="panel">
        <p>
          Owner Console MVP is <strong>single company owner</strong> only. Multi-user RBAC, SSO, and role-based
          screens are explicitly non-goals in the implementation plan.
        </p>
        <p className="muted">
          When needed later: add auth middleware, role claims (owner / operator / viewer), and gate write actions
          (approve, live send) to elevated roles. Keep dry-run default for all non-owner roles.
        </p>
        <ul className="muted">
          <li>No multi-tenant isolation yet</li>
          <li>No SSO / OIDC</li>
          <li>Password gate (Phase 3 optional) is the only access control for now</li>
        </ul>
      </div>
    </div>
  );
}
