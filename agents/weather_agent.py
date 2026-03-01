import json
import os
import re

from llm.ollama_client import OllamaClient
from tools.weather_tool import get_weather


class WeatherAgent:

    def __init__(self):
        self.llm = OllamaClient()

        self.memory_file = "memory/memory.json"
        self.memory = self.load_memory()

        # Restore last city from memory
        self.last_city = self.restore_last_city()

    # -------------------------
    # Memory Handling
    # -------------------------

    def load_memory(self):
        if not os.path.exists(self.memory_file):
            return []

        try:
            with open(self.memory_file, "r") as f:
                return json.load(f)
        except:
            return []

    def save_memory(self):
        with open(self.memory_file, "w") as f:
            json.dump(self.memory, f, indent=2)

    def restore_last_city(self):
        for message in reversed(self.memory):
            if message["role"] == "assistant":
                match = re.search(
                    r"TOOL_CALL: get_weather\((.*?)\)",
                    message["content"]
                )
                if match:
                    return match.group(1).strip()
        return None

    # -------------------------
    # Main Agent Logic
    # -------------------------

    def get_response(self, user_question: str):

        print("Thinking...")

        question_lower = user_question.lower()

        # -------------------------
        # STEP 1 — Detect Weather Intent
        # -------------------------

        weather_keywords = [
            "weather",
            "temperature",
            "rain",
            "umbrella",
            "climate"
        ]

        is_weather_query = any(
            keyword in question_lower
            for keyword in weather_keywords
        )

        # If question is short and contains a city indicator like "in kochi?"
        short_city_pattern = r"^\s*(?:in\s+)?[a-zA-Z\s]+\?\s*$"

        if not is_weather_query and re.match(short_city_pattern, question_lower):
            is_weather_query = True

        # -------------------------
        # STEP 2 — Extract City Deterministically
        # -------------------------

        # Pattern handles:
        # "weather in chennai?"
        # "in kochi?"
        # "at mumbai"
        # "for surat"
        pattern = r"\b(?:in|at|for)\s+([a-zA-Z\s]+?)(?:\?|$)"

        matches = re.findall(pattern, question_lower)

        if matches:
            city = matches[-1].strip().title()
            self.last_city = city
        else:
            city = self.last_city

        if is_weather_query and not city:
            return "Please specify a city."

        # -------------------------
        # STEP 3 — Tool Execution
        # -------------------------

        if is_weather_query:

            print(f"Decision: TOOL_CALL: get_weather({city})")

            weather_data = get_weather(city)

            # Save tool call in memory
            self.memory.append({
                "role": "assistant",
                "content": f"TOOL_CALL: get_weather({city})"
            })

            # -------------------------
            # STEP 4 — LLM Formats Final Answer
            # -------------------------

            final_prompt = f"""
You are a Weather Assistant.

Answer the user's question using ONLY the weather data below.

USER QUESTION:
{user_question}

CITY:
{city}

WEATHER DATA:
{weather_data}

Rules:
- Answer directly
- Do NOT say you lack real-time access
- Do NOT hallucinate
- Do NOT add unrelated suggestions
- Be concise
"""

            final_response = self.llm.ask(final_prompt)

        else:
            # Non-weather question
            final_response = self.llm.ask(user_question)

        # -------------------------
        # STEP 5 — Save Memory
        # -------------------------

        self.memory.append({
            "role": "user",
            "content": user_question
        })

        self.memory.append({
            "role": "assistant",
            "content": final_response
        })

        self.save_memory()

        return final_response