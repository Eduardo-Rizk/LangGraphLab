# cool_classes.py
from pydantic import BaseModel, Field
from typing import List

class Critique(BaseModel):
    """Critique of the travel plan."""
    
    impossible: str = Field(
        description="Critique of what is impossible for the traveler to do, such as recommendations in another city or country."
    )
    redundancy: str = Field(
        description="Critique on whether the plan includes repetitive activities (e.g., too many similar museum visits or food places)."
    )
    alternative_suggestions: str = Field(
        description="Provide alternative options or adjustments to improve feasibility, diversity, or alignment with traveler preferences."
    )
    overbooked_schedule: str = Field(
        description="Critique on whether the plan includes too many activities without time for rest or flexibility."
    )


class DailySchedule(BaseModel):
    """Represents a single day in the travel itinerary."""
    
    day: int = Field(description="The day number in the itinerary.")
    activities: List[str] = Field(
        description="A list of activities planned for the day."
    )
    meal_recommendations: List[str] = Field(
        description="Recommended places to eat throughout the day."
    )


class ToolArgumentsTourist(BaseModel):
    """Arguments for the tool of search tourist attractions."""
    query: str = Field(description=" The name or categories to the place (ex: 'landmarks', 'museums', etc..).")
    location: str = Field(description="Location for the tool.")
    place_type: str = Field(default="tourist_attraction", description="Type of place to search.")
    max_results: int = Field(default=5, description="Maximum number of results.")


class ToolArgumentsRestaurants(BaseModel):
    """Arguments for the tool of search restaurants."""
    query: str = Field(description=" The name or categories to the place (ex: italian food, sushi).")
    location: str = Field(description="The locations to the tools to search. (ex: Paris, Toquio, Rio de Janeiro).")
    place_type: str = Field(default="tourist_attraction", description="Type of place to search.")
    max_results: int = Field(default=5, description="Maximum number of results.")

class Plan(BaseModel):
    """Schedule for the traveler, with daily activities and meal recommendations."""
    
    itinerary: List[DailySchedule] = Field(
        description="List of daily schedules with planned activities and meal recommendations."
    )
    critique: Critique = Field(description="Critique of the overall travel plan.")

    toolArgumentsRestaurants : List[ToolArgumentsRestaurants] = Field(description="Arguments for the tool of search restaurants.")

    toolArgumentsTourist : List[ToolArgumentsTourist] = Field(description="Arguments for the tool of search tourist attractions.")




