# Auditor-IA

Um sistema de análise preliminar de editais de licitação, alimentado por um sistema multiagente com IA generativa, para auxiliar auditores de Tribunais de Contas (TCE).

### Links Vivos

  * **Frontend (Vercel):** `https://auditor-ia-brintell.vercel.app/`
  * **Backend (Render):** `https://auditoria-brintell.onrender.com/docs`

-----

## 1\. Visão Geral do Projeto 🎯

 O **Auditor-IA** automatiza a análise preliminar de editais de licitação em PDF, aumentando a eficiência e a precisão dos auditores.

O sistema funciona da seguinte forma:

1.  O auditor faz o upload de um edital em PDF.
2.  Um sistema orquestrado de 5 agentes de IA entra em ação.
3.  Ao final, o sistema gera um Relatório de Análise Preliminar contendo:
      * Resumo dos pontos-chave do edital.
      * Legislação aplicável ao caso.
      * Jurisprudência relevante (buscada em bases de dados públicas).
      * Identificação de cláusulas de risco ou pontos críticos.

## 2\. Arquitetura e Fluxo de Dados ⚙️

O projeto é dividido em duas aplicações principais: um backend em FastAPI (Python) e um frontend em React (Vite).

### Fluxo dos Agentes (Backend)

O coração do sistema é um fluxo orquestrado (em `backend/src/auditoria_brintell/main.py`) que coordena 5 agentes especializados:

  * **Agente 1: Analista de Documentos**

      * Usa `PyMuPDF` (`fitz`) para extrair o texto completo do PDF enviado.
      * Usa a IA (Gemini) para ler a primeira página e extrair um resumo estruturado (Objeto, Valor, Modalidade, etc.).
      * Localiza e extrai o texto de seções-chave do edital (Objeto, Participação, Apresentação da Proposta, etc.).

  * **Agente 2: Pesquisador de Legislação**

      * Recebe o resumo do Agente 1.
      * Usa a IA (Gemini) para identificar de 3 a 5 artigos principais da Lei nº 14.133/2021 que são relevantes para aquele edital.

  * **Agente 3: Pesquisador de Jurisprudência**

      * Recebe o resumo do Agente 1.
      * Usa a IA (Gemini) para gerar uma query de busca CQL (Contextual Query Language) otimizada.
      * Faz uma chamada `requests` à API pública SRU do **LexML**.
      * Reporta os resultados encontrados (ou informa se não encontrou nada).

  * **Agente 4: Verificador de Conformidade**

      * É o agente principal. Recebe os dados de todos os agentes anteriores (seções do edital, legislação, jurisprudência).
      * Usa a IA (Gemini) com um *prompt* robusto para fazer uma análise crítica, identificando de 3 a 5 pontos de atenção, riscos ou potenciais não conformidades.

  * **Agente 5: Sintetizador de Relatório**

      * Compila todas as saídas (do Agente 1, 2, 3 e 4) num único relatório final formatado em **Markdown**.

### Frontend (React)

  * Uma interface limpa (criada com Vite) que permite o upload do ficheiro PDF.
  * Faz uma chamada `fetch` ao endpoint `/analisar-edital/` do backend, enviando o ficheiro.
  * Recebe o JSON `{ "relatorio_final": "..." }`.
  * Usa a biblioteca `react-markdown` para renderizar (desenhar) a string Markdown formatada de forma legível para o auditor.

-----

## 3\. Stack de Tecnologias 🛠️

| Área | Tecnologia | Motivo |
| :--- | :--- | :--- |
| **Frontend** | React (com Vite) | Interface de utilizador moderna e reativa. |
| | `react-markdown` | Renderizar o relatório final formatado. |
| **Backend** | Python 3 | Linguagem robusta para IA e serviços web. |
| | FastAPI | Framework web moderno e de alta performance para criar a API. |
| | Uvicorn | Servidor ASGI que "serve" a aplicação FastAPI. |
| **Inteligência Artificial**| Google Gemini | Modelo de IA generativa (via `langchain-google-genai`) usado por todos os agentes. |
| **Processamento de Dados**| PyMuPDF (`fitz`)| Extração de texto de alta performance de ficheiros PDF. |
| | LexML (API) | Fonte de dados para jurisprudência. |
| **Hospedagem** | Vercel | Plataforma otimizada para "deploy" contínuo de aplicações frontend (React). |
| | Render | Plataforma de PaaS para "deploy" de serviços web (Python/FastAPI). |

-----

## 4\. Como Rodar Localmente 🖥️

Para executar o projeto na sua máquina, precisará de dois terminais.

### Pré-requisitos

  * Node.js (para o frontend)
  * Python 3.10+ (para o backend)
  * Uma chave de API da Google AI (para o Gemini)

### 1\. Clonar o Repositório

```bash
git clone https://github.com/tiagosdbastos/AuditorIA-Brintell.git
cd AuditorIA-Brintell
```

### 2\. Configurar o Backend (Terminal 1)

1.  **Navegue até à pasta do backend:**

    ```bash
    cd backend
    ```

2.  **Crie e ative um ambiente virtual:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

    *(No Windows, use: `venv\Scripts\activate`)*

3.  **Crie o ficheiro `.env`:**
    Crie um ficheiro chamado `.env` dentro da pasta `backend` e adicione a sua chave da Google:

    ```
    GOOGLE_API_KEY=AIzaSy... (a sua chave secreta)
    ```

4.  **Instale as dependências Python:**
    (Certifique-se que o `backend/requirements.txt` está atualizado)

    ```bash
    pip install -r requirements.txt
    ```

5.  **Inicie o servidor FastAPI:**

    ```bash
    python api.py
    ```

    O backend estará a rodar em `http://localhost:8001` (ou na porta que definiu no `api.py`).

### 3\. Configurar o Frontend (Terminal 2)

1.  **Abra um *novo* terminal.**

2.  **Navegue até à pasta do frontend:**

    ```bash
    cd frontend
    ```

3.  **Instale as dependências Node:**

    ```bash
    npm install
    ```

4.  **Inicie o servidor de desenvolvimento (Vite):**

    ```bash
    npm run dev
    ```

    O frontend estará a rodar em `http://localhost:5173` (ou numa porta similar).

### 4\. (Opcional) Configuração de Proxy Corporativo

Se estiver numa rede corporativa, poderá precisar de configurar o proxy para o `pip`, `npm` e para as variáveis de ambiente (`HTTP_PROXY`, `HTTPS_PROXY`) antes de executar os comandos de instalação e de arranque.

-----

## 5\. Processo de Deploy (Produção) ☁️

Este projeto está configurado para "deploy" contínuo (CI/CD) a partir da *branch* `main`.

### Backend (Render)

  * **Serviço:** Web Service
  * **Root Directory:** `backend`
  * **Build Command:** `pip install -r requirements.txt`
  * **Start Command:** `uvicorn api:app --host 0.0.0.0 --port $PORT`
  * **Variáveis de Ambiente:** É **obrigatório** adicionar a `GOOGLE_API_KEY` no painel "Environment" do Render.

### Frontend (Vercel)

  * **Root Directory:** `frontend`
  * **Build/Start Commands:** O Vercel deteta automaticamente que é um projeto Vite/React.
