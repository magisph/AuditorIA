import React, { useState } from "react";
import Header from "./components/Header";
import Home from "./pages/Home";
import About from "./pages/About";
import ReportView from "./components/ReportView";
import "./styles/base.css";
import "./styles/header.css";
import "./styles/upload.css";
import "./styles/report.css";

export default function App() {
  const [activeTab, setActiveTab] = useState("inicio");
  const [report, setReport] = useState(null);

  const handleReportGenerated = (data) => {
    setReport(data);
    setActiveTab("relatorio");
  };

  const handleNewAnalysis = () => {
    setReport(null);
    setActiveTab("inicio");
  };

  const renderTab = () => {
    switch (activeTab) {
      case "inicio":
        return <Home onReportGenerated={handleReportGenerated} />;
      case "relatorio":
        return <ReportView report={report} onNewAnalysis={handleNewAnalysis} />;
      case "sobre":
        return <About />;
      default:
        return <Home onReportGenerated={handleReportGenerated} />;
    }
  };

  return (
    <div className="app">
      <Header onNavigate={setActiveTab} />
      <main>{renderTab()}</main>
    </div>
  );
}
