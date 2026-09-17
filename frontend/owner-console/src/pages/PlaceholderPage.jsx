import React from "react";
export default function PlaceholderPage({ title, note }) {
  return (
    <div>
      <h2>{title}</h2>
      <p className="muted">{note || "Earlier phase — Phase 4 delivered first."}</p>
      <div className="banner">Scaffold only for this route.</div>
    </div>
  );
}
