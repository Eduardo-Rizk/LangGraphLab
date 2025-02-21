# main.py
from typing import List

from langchain_core.messages import BaseMessage, ToolMessage, AIMessage
from langgraph.graph import END, MessageGraph

from chain import first_responder, revisor

from tools_executor import execute_tools

def stateRevise(state: List[BaseMessage]):
    print("State in revisor:", state)
    return state

MAX_ITERATIONS = 2

builder = MessageGraph()
builder.add_node("draft", first_responder)
builder.add_node("revise", revisor)
builder.add_node("execute_tools", execute_tools)


builder.add_edge("draft", "execute_tools")
builder.add_edge("execute_tools","revise")



def eventloop(state: List[BaseMessage]) -> str:

    count_tools_visits = sum(isinstance(msg, ToolMessage) for msg in state)
    num_iterations = count_tools_visits

    if num_iterations > MAX_ITERATIONS:
        return END

    return "execute_tools"



builder.add_conditional_edges('revise', eventloop)

builder.set_entry_point("draft")

graph = builder.compile()

print(graph.get_graph().draw_mermaid())


res = graph.invoke("I'm going to Paris for 3 days. What should I do?")

print(res[-1].tool_calls[0]["args"]["itinerary"])


