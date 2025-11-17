import React from "react";

export default function Header({ onNavigate }) {
  return (
    <header className="site-header">
      <div className="brand" onClick={() => onNavigate("inicio")}>
        <div className="logo-text">⚖️</div>
        <span className="title">Auditor-IA</span>
      </div>
      <nav className="topnav">
        <button onClick={() => onNavigate("inicio")}>Início</button>
        <button onClick={() => onNavigate("sobre")}>Sobre</button>
      </nav>
    </header>
  );
}
