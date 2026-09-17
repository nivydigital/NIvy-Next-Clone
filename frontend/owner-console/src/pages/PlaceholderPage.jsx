import React from "react";
export default function PlaceholderPage({ title, note }) {
  return (
    <div>
      <h2>{title}</h2>
      <p className="muted">{note}</p>
      <div className="banner">Earlier phase — Phase 4 delivered first.</div>
    </div>
  );
}
