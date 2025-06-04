# importa la classe FastAPI dal framework FastAPI.
from fastapi import FastAPI
from travel_agent_api.routes import chat_router
# importa il middleware.cors che impedisce o consente le richieste da domini diversi da quello dell'API.
from fastapi.middleware.cors import CORSMiddleware
#creazione di un'istanza dell'applicazione FastAPI
app = FastAPI()
#specifico i dns che possono effettuare le richieste
origins = [
"http://127.0.0.1:8000", # Porta standard dell'applicazione foront-end Laravel
"http://localhost:8000" # Alias per localhost e Porta standard dell'applicazione foront-end Laravel
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Domini permessi
    allow_credentials=True, # Permette l'invio di credenziali
    allow_methods=["*"], # Permette tutti i metodi HTTP
    allow_headers=["*"], # Permette tutti gli headers
)

app.include_router(
    chat_router.router, # Il router definito in chat_router.py
    tags=["Chat"], # Tag per la documentazione Swagger
    prefix="/chat" # Prefisso per tutte le route del router
)