# chain.py
from dotenv import load_dotenv

load_dotenv()
import datetime


from langchain_core.messages import HumanMessage

from cool_classes import Plan, ToolArgumentsTourist,ToolArgumentsRestaurants

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")


actor = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are expert trip planner.
            Current time: {time}
            1. {first_instruction};
            2. Reflect on and critique your answer to ensure the plan is optimized for time and preferences.
            3. Recommend additional points of interest or adjustments based on the traveler's profile.
            4. Always suggest a plan structure and separate the plan into days with a list of activities for each day.Including places to eat and to visit thoughout the day.
            5. Always provide per day a place to have breakfast, lunch and dinner.
            6. Provide the arguments to the tools to provide more accurate recommendations.
            """
        ),
        MessagesPlaceholder(variable_name="messages"),
        ("system", "Answer the user's question above using the required format."),
    ]
).partial(time = lambda: datetime.datetime.now().isoformat())





first_responder = actor.partial(
    first_instruction="Provide a detailed plan for the traveler. Considering how much time he has in the place, and IF he has a specific interest of what he wants to do."
) | llm.bind_tools(tools=[Plan], tool_choice= "Plan") 

# executer_tool = actor.partial(
#     first_instruction="Execute the tools based on the arguments given."
# ) | llm.bind_tools(tools=[search_places_tool], tool_choice="auto") 

revise_intructions = """Revise your previous answer using the new information.
    - If has any critique, you should use it to add important information to your answer.
    - Use the results from the tools to provide more accurate recommendations, changing the plan if necessary."""


revisor = actor.partial(first_instruction = revise_intructions) | llm.bind_tools(tools=[Plan], tool_choice="Plan") 


