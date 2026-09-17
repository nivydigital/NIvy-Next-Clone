import React from "react";
import { NavLink, Route, Routes } from "react-router-dom";
import HistoryPage from "./pages/HistoryPage.jsx";
import OpsPage from "./pages/OpsPage.jsx";
import RolesPage from "./pages/RolesPage.jsx";
import ProductionPage from "./pages/ProductionPage.jsx";
import PlaceholderPage from "./pages/PlaceholderPage.jsx";

export default function App() {
  return (
    <div className="layout">
      <aside className="sidebar">
        <h1>Nivy Owner Console</h1>
        <div className="tag">Phase 4 surfaces · single owner</div>
        <nav className="nav">
          <NavLink to="/" end>Dashboard</NavLink>
          <NavLink to="/test/agents">Agent Test Lab</NavLink>
          <NavLink to="/test/workflows">Workflow Test Lab</NavLink>
          <NavLink to="/leads">Leads</NavLink>
          <NavLink to="/approvals">Approvals</NavLink>
          <NavLink to="/history">Run history</NavLink>
          <NavLink to="/ops">Ops / Grafana</NavLink>
          <NavLink to="/roles">Roles</NavLink>
          <NavLink to="/production">Production</NavLink>
          <NavLink to="/settings">Settings</NavLink>
        </nav>
      </aside>
      <main className="main">
        <Routes>
          <Route path="/" element={<PlaceholderPage title="Dashboard" note="Phase 0/3 — health cards when building earlier phases." />} />
          <Route path="/test/agents" element={<PlaceholderPage title="Agent Test Lab" note="Phase 1" />} />
          <Route path="/test/workflows" element={<PlaceholderPage title="Workflow Test Lab" note="Phase 1" />} />
          <Route path="/leads" element={<PlaceholderPage title="Leads" note="Phase 2" />} />
          <Route path="/approvals" element={<PlaceholderPage title="Approvals" note="Phase 2" />} />
          <Route path="/history" element={<HistoryPage />} />
          <Route path="/ops" element={<OpsPage />} />
          <Route path="/roles" element={<RolesPage />} />
          <Route path="/production" element={<ProductionPage />} />
          <Route path="/settings" element={<PlaceholderPage title="Settings" note="Phase 0 — API base URL + dry-run default." />} />
        </Routes>
      </main>
    </div>
  );
}
