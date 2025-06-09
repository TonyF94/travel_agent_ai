from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel , Field
from typing import Optional
from langchain_core.output_parsers import PydanticOutputParser

#struttura dei dati in ingresso definita attraverso pydantic: definisce tutti i parametri necessari per organizzare piani di viaggio:
class TravelPlanInput(BaseModel):
        start_date: str = Field(description="The start date of the trip (YYYY-MM-DD) e.g. 2024-12-13.")#inizio del viaggio
        end_date: str = Field(description="The end date of the trip (YYYY-MM-DD) e.g. 2024-12-19.")#fine del viaggio
        destination: str = Field(description="The destination of the trip.")#destinazione
        adults: Optional[int] = Field(1, description="The number of adults. Defaults to 1.")#numero di adulti default 1
        children: Optional[int] = Field(0, description="The number of children. Defaults to 0.")#numero di bambini default 0
        travel_style: str = Field(description="The style of travel. e.g. adventure, relax,culture, backpacking, luxury, family-friendly.")#stile del viaggio, avventura relax ecc....
        budget: Optional[int] = Field(description="The total budget for the trip.")#budget totale del viaggio
        activities: str = Field(description="The preferred activities. e.g. culture, nature,food, shopping.")#attività preferite da svolgere
        food_restriction: str = Field(description="Any food restrictions. e.g. vegetarian, gluten-free.")#restrizioni alimentari o di altro genere

#gli dico che tutti i parametri definiti prima devono essere dentro il campo params
class TravelPlanInputSchema(BaseModel):
        params : TravelPlanInput

#definisco 3 output di risposta, per la mattina per il pomeriggio e per la sera
class TravelDayOutput(BaseModel):
    morning: str = Field(description="The activities for the morning.")#attività da fare al mattino
    afternoon: str = Field(description="The activities for the afternoon.")#attività da fare al pomeriggio
    evening: str = Field(description="The activities for the evening.")#attività da fare alla sera

class TravelPlanOutput(BaseModel):
    travel_plan: list[TravelDayOutput]


@tool(args_schema=TravelPlanInputSchema)
# gli dico in ingresso avrai un'instanza di TravelPlanInput e darà come output un'instanza di TravelPlanOutput
def chain_travel_plan(params: TravelPlanInput) -> TravelPlanOutput:
    """
    Generates a comprehensive travel plan based on user input parameters.
    Parameters:
    params (TravelPlanInput): The input parameters for the travel plan
    including dates, destination, number of travelers, travel style, budget,
    preferred activities, and any food restrictions.
    Returns:
    TravelPlanOutput: The generated travel plan content.
    """
    model = ChatOpenAI(model_name="gpt-4o")
    system_prompt = f"""
    You are a travel expert.
    Your mission is to provide in-depth content on the topic to create a travel plan.
    The start date of the trip is {params.start_date}.
    The end date of the trip is {params.end_date}.
    The destination of the trip is {params.destination}.
    The number of adults is {params.adults}.
    The number of children is {params.children}.
    The style of travel is {params.travel_style}.
    The total budget for the trip is {params.budget}.
    The preferred activities are {params.activities}.
    Any food restrictions are {params.food_restriction}
    Use emojis to make your answers more engaging and friendly.
    Always strive to be approachable and helpful, offering the
    most accurate and useful information possible to users.
    """
    prompt = ChatPromptTemplate([("human", "{input}")])
    output_parser = PydanticOutputParser(pydantic_object=TravelPlanOutput)
    #la catena : prendi il prompt mandalo al model (ChatGPT) e il risultato va in output_parser (per costruire un oggetto TravelPlanOutput, che è quello che divide la giornata in 3 momenti, mattina pomeriggio e sera)
    chain = prompt | model | output_parser
    #eseguo la catena riempiento dil segnaposto input che avevo messo a riga 63
    result = chain.invoke(input=system_prompt)


    # print("*" * 80)
    # print(output_parser)
    # print("chain_travel_plan")
    # print("*" * 80)
    return result