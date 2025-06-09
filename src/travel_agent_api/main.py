# importa la classe FastAPI dal framework FastAPI.
from fastapi import FastAPI
# Questa riga importa un "router" chiamato chat_router dal file (o modulo) routes che si trova nella cartella travel_agent_api.
from travel_agent_api.routes import chat_router
# importa il middleware.cors che impedisce o consente le richieste da domini diversi da quello dell'API.
from fastapi.middleware.cors import CORSMiddleware
#creazione di un'istanza dell'applicazione FastAPI
app = FastAPI()
#specifico i dns che possono effettuare le richieste
origins = [
"http://127.0.0.1:8000", # dns è porta del server laravel, gli sto dicendo  che può accettare richiesta da questo server, in produzione cambio con i dns e porta reali
"http://localhost:8000" # Alias del dns è porta del server laravel, gli sto dicendo che può accettare richiesta da questo server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Domini permessi
    allow_credentials=True, # Permette l'invio di credenziali
    allow_methods=["*"], # Permette tutti i metodi HTTP (GET, POST, DELETE, PUT)
    allow_headers=["*"], # Permette tutti gli headers
)

# UN ROUTER PERMETTE UN CORRETTO INSTRADAMENTO DELE RICHIESTE, è COME UN VIGILE CHE DIRIGE IL TRAFFICO, SE ARRIVA UNA RICHIESTA GET ALLOA IL ROUTER FA SCATTARE LA FUNZIONE CHE SI OCCUPA DEL GET, SE ARRIVA UNA RICHIESTA POST IL ROUTER FA SCATTARE LA FUNZIONE CHE SI OCCUPA DEL POST
app.include_router(
    chat_router.router, # Il router definito in chat_router.py
    tags=["Chat"], # Tag per la documentazione Swagger
    prefix="/chat" # Prefisso per tutte le route del router
)