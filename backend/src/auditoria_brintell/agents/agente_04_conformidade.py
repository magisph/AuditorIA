import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import json


def verificar_conformidade(
    secoes_extraidas: dict, legislacao_aplicavel: str, jurisprudencia_relevante: str
) -> str | None:
    print("AGENTE 4: Iniciando verificação de conformidade...")

    load_dotenv()
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        print(
            "ERRO (Agente 3): Chave GOOGLE_API_KEY não encontrada."
        )  # Corrigido para Agente 3
        return None
    llm = ChatGoogleGenerativeAI(
        google_api_key=google_api_key,
        model="gemini-2.5-flash",
        temperature=0.0,
        convert_system_message_to_human=True,
    )
    secoes_formatadas = json.dumps(secoes_extraidas, indent=2, ensure_ascii=False)

    prompt_analise = f"""
    Você é um Auditor de Controle Externo experiente do Tribunal de Contas (TCE), especializado em análise de editais de licitação, com foco na Lei nº 14.133/2021.

Sua tarefa é realizar uma análise crítica preliminar das seções de um edital, cruzando-as com a legislação aplicável e jurisprudência relevante.

---

Documentos Fornecidos:

1. Seções extraídas do edital:
   {secoes_formatadas}

2. Legislação aplicável:
   {legislacao_aplicavel}

3. Jurisprudência relevante:
   {jurisprudencia_relevante}

---

Instruções:

- Leia atentamente cada seção do edital.
- Verifique aderência à Lei 14.133/2021 e à jurisprudência.
- Identifique de 3 a 5 pontos principais que merecem atenção, podendo ser:
  • cláusulas restritivas à competitividade,
  • exigências desproporcionais,
  • indícios de direcionamento,
  • omissões relevantes,
  • incompatibilidades legais.

Para cada ponto identificado:
- descreva o risco ou potencial não conformidade,
- mencione a seção do edital analisada,
- relacione com o artigo da lei ou jurisprudência.

---

Formato da resposta (obrigatório):

1. [Ponto de atenção / risco]
   Justificativa breve, citando Seção X do edital e/ou Art. Y da Lei 14.133/2021 (ou jurisprudência Z).

2. [Ponto de atenção / risco]
   Justificativa breve [...]

(3 a 5 itens)

- Não faça introduções ou conclusões.
- Seja direto e objetivo.
- Se não houver não conformidades claras, liste os pontos que exigem verificação cuidadosa.
    """

    print("AGENTE 4: Enviando dados para análise de conformidade pela IA...")

    try:
        analise_riscos = llm.invoke(prompt_analise).content
        print("AGENTE 4: Análise de conformidade recebida.")
        return analise_riscos  # type: ignore
    except Exception as e:
        print(
            f"ERRO (Agente 4): Falha ao realizar análise de conformidade. Detalhe: {e}"
        )
        # Retorne None
        return None
