from llm.ollama_client import OllamaClient

client = OllamaClient()

response = client.ask("Hello, who are you?")

print(response)
