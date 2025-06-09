import requests
from datetime import datetime
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

#IMPORT DEI VARI TOOLS
from travel_agent_api.tools.flights_finder import flights_finder
from travel_agent_api.tools.hotels_finder import hotels_finder
from travel_agent_api.tools.chain_historical_expert import chain_historical_expert
from travel_agent_api.tools.chain_travel_plan import chain_travel_plan

# IMPORTO I TEMPLATE DI RISPOSTA PER HOTEL VOLI E ITINERARI
from travel_agent_api.templates.output_templates import FLIGHTS_OUTPUT, HOTELS_OUTPUT, TRAVEL_PLAN_OUTPUT


class Agent:
    def __init__(self):
        self.current_datetime = datetime.now()
        self.location = self.get_user_location()  # <-- qui

        self.model = ChatOpenAI(model_name="gpt-4o")
        self.tools = [
            chain_historical_expert,
            flights_finder,
            hotels_finder,
            chain_travel_plan,
        ]
        self.agent_executor = create_react_agent(self.model , self.tools)

    # Metodo di istanza: serve il "self"
    def get_user_location(self):
        try:
            response = requests.get("https://ipinfo.io/json")
            data = response.json()
            loc = data.get("loc")
            if loc:
                lat, lon = loc.split(",")
                return {"lat": lat, "lon": lon}
        except Exception as e:
            print("Errore:", e)
        return None

    def run(self, messages : list):
        SYSTEM_PROMPT = f"""
            Sei un travel planner. Il tuo compito e' organizzare il viaggio per l'utente.
            Aggiungi delle emojis per rendere il tuo output piu' interessante.
            La data di oggi e' {self.current_datetime}.
            Mi trovo a latitudine {self.location['lat'] if self.location else 'sconosciuta'} e longitudine {self.location['lon'] if self.location else 'sconosciuta'}.
            Usa le seguenti istruzioni per creare un output:
            Esempio Ouput Voli:
            {FLIGHTS_OUTPUT}
            Esempio Output Hotel:
            {HOTELS_OUTPUT}
            Esempio di Output Viaggio:
            {TRAVEL_PLAN_OUTPUT}
            """
        conversation_history = [{"role" : "system" , "content" : SYSTEM_PROMPT}] + messages
        response = self.agent_executor.invoke({"messages" : conversation_history})
        return response["messages"][1:]
