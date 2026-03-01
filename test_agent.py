from agents.weather_agent import WeatherAgent

agent = WeatherAgent()

question = "Should I carry an umbrella in Mumbai?"

response = agent.get_response(question)

print(response)
