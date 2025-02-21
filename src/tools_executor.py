#tool_executor.py
import os
import requests
import json
from dotenv import load_dotenv
from typing import List, Dict
from collections import defaultdict
from langgraph.prebuilt import ToolInvocation, ToolExecutor
from langchain_core.messages import BaseMessage, ToolMessage, AIMessage
from langchain_core.output_parsers.openai_tools import JsonOutputToolsParser
# Carregar variáveis do .env
load_dotenv()

# Obter a API Key do ambiente
GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")


from langchain_core.tools import tool

@tool
def search_places_tool(query: str, location: str, place_type: str = "tourist_attraction", max_results: int = 5):
    """
    Faz uma busca na Google Places API para encontrar locais com base na categoria.

    Args:
        query (str): Nome ou tipo de lugar a buscar (ex: "museums", "sushi", "restaurants").
        location (str): Localização da busca (ex: "Paris, France").
        place_type (str): Tipo do local (ex: "tourist_attraction", "restaurant").
        max_results (int): Número máximo de resultados.

    Returns:
        Lista de dicionários com detalhes dos locais encontrados.
    """
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "query": f"{query} in {location}",
        "type": place_type,
        "key": GOOGLE_PLACES_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "results" in data:
        return [
            {
                "name": place.get("name"),
                "address": place.get("formatted_address"),
                "rating": place.get("rating"),
                "user_ratings_total": place.get("user_ratings_total"),
                "category": place_type  
            }
            for place in data["results"][:max_results]
        ]
    return []
tool_executor = ToolExecutor([search_places_tool])
def execute_tools(state: List[BaseMessage]) -> List[BaseMessage]:
    tool_invocation: AIMessage = state[-1]

    parser = JsonOutputToolsParser(return_id = True)
    all_calls = parser.invoke(tool_invocation)
    # Ex.: all_calls => [ { "args": {...}, "type": "Plan" } ]

    tool_messages = []

   

    ids = []
    tool_invocation = []

    for call_data in all_calls:
        
        parsed_args = call_data.get("args", {})
        args_Restaurants = parsed_args.get("toolArgumentsRestaurants", [])
        args_Tourists = parsed_args.get("toolArgumentsTourist", [])

        for i, call in enumerate(args_Restaurants):
            tool_invocation.append(ToolInvocation(
                tool = "search_places_tool",
                tool_input = call,
            ))
            ids.append(call_data["id"])
        for i, call in enumerate(args_Tourists):
            tool_invocation.append(ToolInvocation(
                tool = "search_places_tool",
                tool_input = call,
            ))
            ids.append(call_data["id"])
    
    
    outputs = tool_executor.batch(tool_invocation)
    


    outputs_map = defaultdict(dict)

    for id, output, tool_invocation in zip(ids,outputs,tool_invocation):
        key = json.dumps(tool_invocation.tool_input, sort_keys=True)
        outputs_map[id][key] = output

    tool_messages = []

    for id, query_outputs in outputs_map.items():
        tool_messages.append(ToolMessage(
            content = json.dumps(query_outputs), tool_call_id = id))
        
    return tool_messages








