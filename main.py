from graph.weather_graph import build_graph


def main():

    graph = build_graph()

    print("Agentic Weather Intelligence System (LangGraph)")
    print("Type 'exit' to quit\n")

    # ✅ Persistent session state
    state = {
        "user_question": "",
        "is_weather_query": False,
        "city": "",
        "weather_data": "",
        "final_response": ""
    }

    while True:

        user_input = input("Ask: ")

        if user_input.lower() == "exit":
            break

        # Update only the question
        state["user_question"] = user_input

        # Invoke graph with SAME state object
        state = graph.invoke(state)

        print("\nAnswer:", state["final_response"], "\n")


if __name__ == "__main__":
    main()