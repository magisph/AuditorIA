import React, { useRef } from "react";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";
import ReportCard from "./ReportCard";
import ReactMarkdown from "react-markdown";

export default function ReportView({ report, onNewAnalysis }) {
  const reportRef = useRef();

  const exportToPDF = async () => {
    const element = reportRef.current;
    const canvas = await html2canvas(element, { scale: 2 });
    const imgData = canvas.toDataURL("image/png");
    const pdf = new jsPDF("p", "mm", "a4");
    const width = pdf.internal.pageSize.getWidth();
    const height = (canvas.height * width) / canvas.width;
    pdf.addImage(imgData, "PNG", 0, 0, width, height);
    pdf.save("relatorio_auditorIA.pdf");
  };

  return (
    <section className="report-view">
      <h2>📋 Relatório de Análise</h2>

      <div className="report-content" ref={reportRef}>
        <div className="report-columns">
          <ReactMarkdown>{report.relatorio_final}</ReactMarkdown>
        </div>
      </div>

      <div className="controls">
        <button className="btn pdf" onClick={exportToPDF}>
          📄 Exportar PDF
        </button>
        <button className="btn secondary" onClick={onNewAnalysis}>
          🔁 Nova Análise
        </button>
      </div>
    </section>
  );
}
