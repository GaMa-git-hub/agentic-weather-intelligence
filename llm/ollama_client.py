import ollama


class OllamaClient:
    def __init__(self, model="gemma:2b"):
        """
        Initialize Ollama client with model name.
        """
        self.model = model

    def ask(self, prompt: str) -> str:
        """
        Send prompt to Ollama and return response.
        """

        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return response["message"]["content"]

        except Exception as e:
            return f"Ollama Error: {str(e)}"
