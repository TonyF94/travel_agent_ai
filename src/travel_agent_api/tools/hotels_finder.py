import os
from langchain_core.tools import tool
from serpapi import GoogleSearch
from dotenv import load_dotenv
from pydantic import BaseModel , Field
from typing import Optional
from enum import IntEnum

load_dotenv()

#stelle dell'hotel
class HotelClassEnum(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5

#struttura dei dati in ingresso definita attraverso pydantic: definisce tutti i parametri necessari per una ricerca hotel:
class HotelsInput(BaseModel):
    q: str = Field(description="Location of the hotel.") #dove si trova l'hotel
    check_in_date: str = Field(description="The outbound date (YYYY-MM-DD) e.g. 2024-12-13.") #data check_in
    check_out_date: str = Field(description="The return date (YYYY-MM-DD) e.g. 2024-12-19.") #data check_out
    adults: Optional[int] = Field(1, description="The number of adults. Defaults to 1.") #numero di adulti default 1
    children: Optional[int] = Field(0, description="The number of children. Defaults to 0.") #numero di bambini default 0
    hotel_class: Optional[int] = Field(2, description="The hotel class avaible from 2 to 5 .Defaults to 2.") #stelle dell'hotel default 2

#gli dico che tutti i parametri definiti prima devono essere dentro il campo params
class HoltesInputSchema(BaseModel):
    params : HotelsInput

@tool(args_schema=HoltesInputSchema)
def hotels_finder(params: HotelsInput):
    """
    This tool uses the SerpApi Google Hotels API to retrieve hotels info.

    Parameters:
        q (str): Location of the hotel.
        check_in_date (str): The outbound date (YYYY-MM-DD) e.g. 2024-12-13.
        check_out_date (str): The return date (YYYY-MM-DD) e.g. 2024-12-19.
        adults (int): The number of adults. Defaults to 1.
        children (int): The number of children. Defaults to 0.
        hotel_class (int): The hotel class available from 2 to 5. Defaults to 2.
    Returns:
        dict: A dictionary containing the hotels info. If the API call fails, it returns the
        error message as a string.
    """

    params = {
        "api_key": os.getenv("SERPAPI_API_KEY"),
        "engine": "google_hotels",
        "hl": "it", #risultati in italiano
        "gl": "it", #risultati in italiano
        "currency": "EUR",
        "q": params.q,
        "check_in_date": params.check_in_date,
        "check_out_date": params.check_out_date,
        "adults": params.adults,
        "children": params.children,
        "hotel_class": params.hotel_class,
        "num": 6
    }
    try:
        search = GoogleSearch(params)
        results = search.get_dict()["properties"]
    except Exception as e:
            print("Error:", e)
            results = str(e)


            # print("*" * 80)
            # print("hotels_finder")
            # print("*" * 80)
            return results