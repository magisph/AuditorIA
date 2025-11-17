import { useState } from "react";
import UploadArea from "../components/UploadArea";

export default function Home({ onReportGenerated }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

  const handleAnalyze = async () => {
    if (!file) {
      alert("Por favor, selecione um arquivo PDF antes de continuar.");
      return;
    }
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${API_URL.replace(/\/$/, "")}/analisar-edital/`, {
        method: "POST",
        body: formData,
      });

      const text = await res.text(); // lê como texto primeiro
      let data;
      try {
        data = text ? JSON.parse(text) : null;
      } catch (err) {
        data = { raw: text };
      }

      if (!res.ok) {
        // tenta extrair mensagem útil do JSON ou do texto cru
        const errMsg = (data && (data.detail || data.error || data.message)) || text || `Erro ${res.status}`;
        throw new Error(errMsg);
      }

      // aqui data é o JSON parseado (ou objeto com raw)
      onReportGenerated?.(data);
    } catch (error) {
      console.error("Erro ao chamar API:", error);
      alert(`Erro: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="home">
      <h1>Análise Inteligente de Editais</h1>
      <p>
        Faça upload de um edital em PDF para que o Auditor-IA gere um relatório
        automático com resumo, riscos e legislação aplicável.
      </p>

      <UploadArea onFileSelected={setFile} />

      <div className="controls">
        <button
          className="btn primary"
          disabled={!file || loading}
          onClick={handleAnalyze}
        >
          {loading ? "Analisando..." : "Analisar Edital"}
        </button>
      </div>
    </section>
  );
}
