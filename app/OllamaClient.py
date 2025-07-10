import ollama
import os


class OllamaClient:
    def __init__(self, host: str, model: str):
        self.__host = os.getenv(host)
        self.__client = ollama.Client(host=self.__host)
        self.__model = model
        self.__persona = None
        self.__conversation_history = []

        try:
            self.__client.show(self.__model)

        except ollama.ResponseError:
            print(f"Downloading {self.__model}...")
            try:
                self.__client.pull(self.__model)
                print(f"{self.__model} download completed successfully.")

            except Exception as e:
                print(f"Failed to download {self.__model}: {e}")
                raise

    def set_persona(self, desc: str) -> None:
        self.__persona = desc

    def ask(self, prompt: str) -> str:
        messages = []

        if self.__persona:
            messages.append({"role": "system", "content": self.__persona})
        messages.extend(self.__conversation_history)
        messages.append({"role": "user", "content": prompt})

        try:
            response = self.__client.chat(
                model=self.__model,
                messages=messages,
            )

            reply = str(response["message"]["content"])
            self.__conversation_history.extend(
                [
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": reply},
                ]
            )

            return reply

        except ollama.ResponseError as e:
            print(f"Error getting a response: {e}")
            return "An error occurred while processing chat request."

    def clear_history(self):
        self.__conversation_history = []
