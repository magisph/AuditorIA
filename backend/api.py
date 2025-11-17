import logging
import os
import shutil
import tempfile

import uvicorn  # type: ignore
from fastapi import FastAPI, File, HTTPException, UploadFile  # type: ignore
from fastapi.middleware.cors import CORSMiddleware
from src.auditoria_brintell.main import executar_fluxo_auditoria

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


app = FastAPI(title="Auditor-IA API")
# Lista de "origens" (endereços) que têm permissão para aceder à tua API
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://localhost",
    "https://auditor-ia-brintell.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permite as origens da lista
    allow_credentials=True,  # Permite cookies (útil para o futuro)
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)


@app.get("/")
def ler_raiz():
    return {"message": "Olá, Auditor-IA! O servidor está no ar."}


@app.post("/analisar-edital/")
async def analisar_edital(file: UploadFile = File(...)):
    temp_pdf_path = None
    try:  # tente
        temp_dir = "data/uploads"
        os.makedirs(temp_dir, exist_ok=True)  # criar o diretori uploads
        temp_pdf_path = os.path.join(  # type: ignore
            temp_dir, file.filename  # type: ignore
        )  # cria o caminho do arquivo
        with open(temp_pdf_path, "wb") as f:  # abra o arquivo
            shutil.copyfileobj(file.file, f)  # pegue o arquivo
        relatorio = executar_fluxo_auditoria(temp_pdf_path)  # execute o fluxo
        return {"relatorio_final": relatorio}  # retorne
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if temp_pdf_path is not None and os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)


if __name__ == "__main__":
    print("Iniciando servidor FastAPI em http://localhost:8000")
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
