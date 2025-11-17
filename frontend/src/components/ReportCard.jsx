import React from "react";

export default function ReportCard({ title, children, className = "" }) {
  return (
    <div className={`report-card ${className}`}>
      <h3>{title}</h3>
      <div className="card-body">{children}</div>
    </div>
  );
}
