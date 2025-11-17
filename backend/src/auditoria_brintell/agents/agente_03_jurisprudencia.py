import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import requests
import xmltodict
from ..external_apis.lexml import LexmlAcervo


def _criar_query_cql(contexto_objeto: str, llm: ChatGoogleGenerativeAI) -> str:

    print("AGENTE 3 (IA): Gerando query CQL para o LexML...")

    prompt_cql = f"""
    Você é um assistente especialista em consultas jurídicas para o LexML (API SRU).
    Sua tarefa é converter um objeto de licitação em uma query de busca (CQL) SIMPLES E EFICAZ para encontrar JURISPRUDÊNCIA relevante no LexML.

    Regras de Construção da Query:
    - **Selecione APENAS os 2 ou 3 termos MAIS IMPORTANTES** do objeto. # <--- NOVA REGRA
    - **NÃO use índices** (como dc.title=, texto=, etc.). Faça uma busca geral.
    - Inclua o termo **jurisprudencia** combinado com AND aos termos selecionados.
    - Combine os termos selecionados e 'jurisprudencia' com o operador **AND**.
    - Utilize aspas duplas para termos compostos (ex: "apoio técnico").
    - **NÃO use parênteses** ao redor da query inteira.
    - A saída deve ser **apenas a string da query CQL**.

    Regras de Apresentação:
    - Retorne **somente** a query final, em uma única linha.
    - Exemplo de saída (para objeto sobre apoio técnico): "apoio técnico" AND fiscalização AND jurisprudencia
    - Exemplo de saída (para objeto sobre engenharia consultiva): "engenharia consultiva" AND supervisão AND jurisprudencia # <--- MAIS EXEMPLOS

    Objeto da Licitação:
    ---
    {contexto_objeto}
    ---

    Query CQL:
    """

    try:
        query_gerada = llm.invoke(prompt_cql).content
        print(f"AGENTE 3 (IA): Query gerada: {query_gerada}")
        return query_gerada  # type: ignore
    except Exception as e:
        print(f"ERRO (Agente 3 - IA): Falha ao gerar query. {e}")
        return "tipo=jurisprudencia"


def _formatar_resultados_lexml(
    resultados_json: list, llm: ChatGoogleGenerativeAI
) -> str:

    print("AGENTE 3 (IA): Formatando resultados do LexML...")

    primeiros_resultados = json.dumps(resultados_json[:3], ensure_ascii=False, indent=2)
    prompt_formatacao = f"""
    Você é um assistente especialista em consultas jurídicas para o LexML (API SRU).
    Sua tarefa é converter um objeto de licitação em uma query de busca (CQL) otimizada para encontrar JURISPRUDÊNCIA relevante no LexML.

    Regras de Construção da Query:
    - Utilize o índice **ementa** para buscar os termos.
    - Inclua o termo **jurisprudencia** DENTRO da busca no índice 'ementa', combinado com AND. # <--- MUDANÇA PRINCIPAL
    - Combine os principais termos-chave do objeto de licitação com o operador **AND**, também dentro da busca em 'ementa'.
    - Utilize aspas duplas para termos compostos (exemplo: "apoio técnico").
    - Coloque toda a expressão de busca do índice entre parênteses. # <--- MUDANÇA IMPORTANTE
    - Evite palavras genéricas (ex: "contratação", "serviço", "objeto").
    - A saída deve ser **apenas a string da query CQL**.

    Regras de Apresentação:
    - Retorne **somente** a query final, em uma única linha.
    - Exemplo de saída: ementa=("apoio técnico" AND fiscalização AND jurisprudencia) # <--- NOVO EXEMPLO

    Objeto da Licitação:
    ---
    {contexto_objeto}
    ---

    Query CQL:
    """

    try:
        resposta_formatada = llm.invoke(prompt_formatacao).content
        return resposta_formatada  # type: ignore
    except Exception as e:
        print(f"ERRO (Agente 3 - IA): Falha ao formatar. {e}")
        return "Erro ao formatar resultados da jurisprudência."


# --- Função Principal do Agente ---
def pesquisar_jurisprudencia(contexto_objeto: str) -> str | None:
    print("AGENTE 3: Iniciando pesquisa de jurisprudência no LexML...")

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

    # --- Etapa A: Gerar a Query ---
    query_cql = _criar_query_cql(contexto_objeto, llm)
    if not query_cql:
        return "Falha ao gerar query de busca para jurisprudência."

    # --- Etapa B: Buscar DIRETAMENTE no LexML (sem a classe LexmlAcervo) ---
    try:

        base_url = "https://www.lexml.gov.br/busca/SRU"
        params = {
            "operation": "searchRetrieve",
            "version": "1.1",
            "query": query_cql,
            "maximumRecords": "5",
        }

        print(f"AGENTE 3 (LexML): Executando busca direta com query: {query_cql}")
        response = requests.get(
            base_url,
            params=params,
            timeout=(10, 30),
            proxies={"http": None, "https": None},  # type: ignore
        )
        response.raise_for_status()
        data_dict = xmltodict.parse(response.content)

        # --- Processar os Resultados ---
        records = (
            data_dict.get("searchRetrieveResponse", {})
            .get("records", {})
            .get("record", [])
        )
        if not isinstance(records, list):
            records = [records]

        print(
            f"AGENTE 3 (LexML): Busca concluída. {len(records)} resultados encontrados."
        )

        if not records:
            return "Nenhuma jurisprudência relevante encontrada no LexML para esta consulta."

        # --- Etapa C: Formatar a Saída ---)
        relatorio_formatado = _formatar_resultados_lexml(records, llm)
        return relatorio_formatado

    except requests.exceptions.RequestException as e:
        print(
            f"ERRO (Agente 3 - Request): Falha ao conectar com API do LexML. Detalhe: {e}"
        )
        return "Erro de conexão ao buscar jurisprudência no LexML."
    except xmltodict.expat.ExpatError as e:  # type: ignore
        print(
            f"ERRO (Agente 3 - XML): Falha ao processar XML da resposta do LexML. Detalhe: {e}"
        )
        return "Erro ao processar a resposta da busca de jurisprudência."
    except Exception as e:
        print(f"ERRO (Agente 3 - Geral): Falha inesperada. Detalhe: {e}")
        return "Erro inesperado ao buscar ou processar jurisprudência."
