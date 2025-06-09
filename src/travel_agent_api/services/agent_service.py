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
        self.model = ChatOpenAI(model_name="gpt-4o")
        self.tools = [
        chain_historical_expert,
        flights_finder,
        hotels_finder,
        chain_travel_plan,
        ]
        self.agent_executor = create_react_agent(self.model , self.tools)
        pass

    def run(self, messages : list):
        SYSTEM_PROMPT = f"""
            Sei un travel planner. Il tuo compito e' organizzare il viaggio per l'utente.
            Aggiungi delle emojis per rendere il tuo output piu' interessante.
            La data di oggi e' {self.current_datetime}
            Usa le seguenti istruzioni per creare un output:
            Esempio Ouput Voli:
            {FLIGHTS_OUTPUT}
            Esempio Output Hotel:
            {HOTELS_OUTPUT}
            Esempio di Output Viaggio:
            {TRAVEL_PLAN_OUTPUT}
            """
        convesation_history = [{"role" : "system" , "content" : SYSTEM_PROMPT}] + messages
        response = self.agent_executor.invoke({"messages" : convesation_history})
        return response["messages"][1:]