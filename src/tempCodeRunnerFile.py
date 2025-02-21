# main.py
from typing import List

from langchain_core.messages import BaseMessage, ToolMessage, AIMessage
from langgraph.graph import END, MessageGraph

from chain import first_responder, revisor, executer_tool



MAX_ITERATIONS = 2

builder = MessageGraph()
builder.add_node("draft", first_responder)
builder.add_node("revise", revisor)
builder.add_node("execute_tools", executer_tool)

builder.add_edge("draft", "execute_tools")
builder.add_edge("execute_tools","revise")

def eventloop(state: List[BaseMessage]) -> str:
    last_message = state[-1]

    # Se não houver mais ferramentas a serem chamadas, encerramos
    if isinstance(last_message, AIMessage) and "tool_calls" not in last_message.additional_kwargs:
        return END

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

print(res)

