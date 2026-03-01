from graph.weather_graph import build_graph

graph = build_graph()

result = graph.invoke({
    "user_question": "what is weather in chennai?",
    "is_weather_query": False,
    "city": "",
    "weather_data": "",
    "final_response": ""
})

print(result["final_response"])