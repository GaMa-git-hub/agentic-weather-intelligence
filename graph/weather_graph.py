from typing import TypedDict
import re

from langgraph.graph import StateGraph, END
from tools.weather_tool import get_weather
from llm.ollama_client import OllamaClient


# -------------------------
# Define Graph State
# -------------------------

class WeatherState(TypedDict):
    user_question: str
    is_weather_query: bool
    city: str
    weather_data: str
    final_response: str


llm = OllamaClient()


# -------------------------
# Node 1 — Intent Detection
# -------------------------

def intent_node(state: WeatherState):

    question = state["user_question"].strip().lower()

    weather_keywords = [
        "weather",
        "temperature",
        "rain",
        "umbrella",
        "climate"
    ]

    # Normal weather detection
    is_weather = any(word in question for word in weather_keywords)

    # Short follow-up like "in kochi?"
    short_pattern = r"^\s*(?:in\s+)?[a-zA-Z\s]+\?\s*$"

    if not is_weather and re.match(short_pattern, question):
        is_weather = True

    # ✅ NEW: single-word city input
    single_word_pattern = r"^[a-zA-Z\s]{2,20}$"

    if not is_weather and re.match(single_word_pattern, question):
        # treat as city follow-up
        is_weather = True

    state["is_weather_query"] = is_weather

    return state

# -------------------------
# Node 2 — City Extraction
# -------------------------

def city_node(state: WeatherState):

    if not state["is_weather_query"]:
        return state

    # Normalize question
    question = state["user_question"].strip().lower()

    # Remove punctuation like ?, ., !
    clean_question = re.sub(r"[^\w\s]", "", question)

    # -------------------------
    # Case 1: "weather in city"
    # -------------------------
    pattern = r"\b(?:in|at|for)\s+([a-zA-Z\s]+)$"
    match = re.search(pattern, clean_question)

    if match:
        city = match.group(1).strip().title()
        state["city"] = city
        return state

    # -------------------------
    # Case 2: single city word
    # -------------------------
    if re.match(r"^[a-zA-Z\s]{2,20}$", clean_question):
        city = clean_question.title()
        state["city"] = city
        return state

    return state


# -------------------------
# Node 3 — Weather Tool
# -------------------------

def weather_tool_node(state: WeatherState):

    if not state["is_weather_query"]:
        return state

    city = state["city"]

    if not city:
        state["final_response"] = "Please specify a city."
        return state

    print(f"Decision: TOOL_CALL: get_weather({city})")

    weather_data = get_weather(city)

    state["weather_data"] = weather_data

    return state


# -------------------------
# Node 4 — Response Generation
# -------------------------

def response_node(state: WeatherState):

    if not state["is_weather_query"]:
        state["final_response"] = llm.ask(state["user_question"])
        return state

    prompt = f"""
You are a Weather Assistant.

Answer the user's question using ONLY the weather data below.

USER QUESTION:
{state['user_question']}

CITY:
{state['city']}

WEATHER DATA:
{state['weather_data']}

Rules:
- Answer directly
- Do NOT say you lack real-time access
- Do NOT hallucinate
- Be concise
"""

    final_response = llm.ask(prompt)

    state["final_response"] = final_response

    return state


# -------------------------
# Build Graph
# -------------------------

def build_graph():

    graph = StateGraph(WeatherState)

    graph.add_node("intent", intent_node)
    graph.add_node("city", city_node)
    graph.add_node("weather_tool", weather_tool_node)
    graph.add_node("response", response_node)

    graph.set_entry_point("intent")

    graph.add_edge("intent", "city")
    graph.add_edge("city", "weather_tool")
    graph.add_edge("weather_tool", "response")
    graph.add_edge("response", END)

    return graph.compile()