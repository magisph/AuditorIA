import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# A linha de definição da função corrigida:
def pesquisar_legislacao(analise_agente_1: str) -> str | None: #Essa linha
    print("AGENTE 2: Iniciando pesquisa de legislação...")
    load_dotenv()
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        print("ERRO (Agente 2): Chave GOOGLE_API_KEY não encontrada.")
        return None
    llm = ChatGoogleGenerativeAI(
        google_api_key=google_api_key,
        model="gemini-2.5-flash",
        temperature=0.0,
        convert_system_message_to_human=True,
    )

    prompt_legislacao = f"""
    Você é um assistente especialista na Lei de Licitações (Lei nº 14.133/2021).
    Sua tarefa é analisar o conteúdo de um edital e identificar os principais artigos ou seções da Lei que um auditor deve verificar.

    Regras de Análise:
    - Baseie-se **exclusivamente** na análise do edital fornecida.
    - Identifique de **3 a 5 artigos ou seções** da Lei nº 14.133/2021 que sejam diretamente relevantes ao contexto apresentado.
    - Para cada artigo ou seção, apresente:
        • O número do artigo/seção
        • Uma justificativa curta e objetiva explicando sua importância para o caso
    - O foco deve ser em pontos de controle, conformidade, transparência, planejamento, julgamento e execução contratual.
    - Não cite artigos genéricos sem relação direta com o conteúdo do edital.
    - Não invente informações ou trechos inexistentes na lei.

    Regras de Apresentação:
    - Responda **exclusivamente** no formato de lista numerada, com o seguinte padrão:
        1. Art. [número] — [breve justificativa]
        2. Art. [número] — [breve justificativa]
        ...
    - Não inclua introduções, comentários adicionais, conclusões, opiniões ou explicações fora do formato.
    - Não utilize formatação adicional (como negrito, itálico ou títulos).
    - Não faça citações literais extensas da lei — apenas mencione o número do artigo e uma síntese da sua pertinência.
    - Não insira frases como “de acordo com”, “conforme a análise acima”, “em suma” ou similares.
    - Não insira mais de 5 itens.

    Análise do Edital:
    ---
    {analise_agente_1}
    ---

    Responda **somente** com a lista solicitada, seguindo rigorosamente o formato indicado.
"""


    print("AGENTE 2: Enviando pergunta sobre legislação para a IA...")
    try:
        # Chama a IA e guarda a resposta completa
        resposta_legislacao = llm.invoke(prompt_legislacao)
        print("AGENTE 2: Resposta da IA sobre legislação recebida.") # Ajustei a mensagem

        # ---> CORREÇÃO: Retorna o CONTEÚDO da resposta em caso de sucesso <---
        return resposta_legislacao.content

    except Exception as e:
        # Imprime uma mensagem de erro detalhada
        print(f"ERRO (Agente 2): Problema ao se comunicar com a API. Detalhe: {e}") # Ajustei a mensagem

        # ---> CORREÇÃO: Retorna None em caso de erro <---
        return None
