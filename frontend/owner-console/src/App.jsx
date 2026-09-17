import { NavLink, Route, Routes } from "react-router-dom";
import Dashboard from "./pages/Dashboard.jsx";
import AgentLab from "./pages/AgentLab.jsx";
import WorkflowLab from "./pages/WorkflowLab.jsx";
import Leads from "./pages/Leads.jsx";
import Approvals from "./pages/Approvals.jsx";
import Settings from "./pages/Settings.jsx";
import HistoryPage from "./pages/HistoryPage.jsx";
import OpsPage from "./pages/OpsPage.jsx";
import RolesPage from "./pages/RolesPage.jsx";
import ProductionPage from "./pages/ProductionPage.jsx";

const links = [
  { to: "/", label: "Dashboard", end: true },
  { to: "/test/agents", label: "Agent Lab" },
  { to: "/test/workflows", label: "Workflow Lab" },
  { to: "/leads", label: "Leads" },
  { to: "/approvals", label: "Approvals" },
  { to: "/history", label: "History" },
  { to: "/ops", label: "Ops" },
  { to: "/roles", label: "Roles" },
  { to: "/production", label: "Production" },
  { to: "/settings", label: "Settings" },
];

export default function App() {
  return (
    <div className="layout">
      <aside className="sidebar">
        <h1>Nivy Owner Console</h1>
        <div className="tag">Company owner · dry-run default</div>
        <nav className="nav">
          {links.map((l) => (
            <NavLink key={l.to} to={l.to} end={l.end} className={({ isActive }) => (isActive ? "active" : undefined)}>
              {l.label}
            </NavLink>
          ))}
        </nav>
      </aside>
      <main className="main">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/test/agents" element={<AgentLab />} />
          <Route path="/test/workflows" element={<WorkflowLab />} />
          <Route path="/leads" element={<Leads />} />
          <Route path="/approvals" element={<Approvals />} />
          <Route path="/history" element={<HistoryPage />} />
          <Route path="/ops" element={<OpsPage />} />
          <Route path="/roles" element={<RolesPage />} />
          <Route path="/production" element={<ProductionPage />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </main>
    </div>
  );
}
