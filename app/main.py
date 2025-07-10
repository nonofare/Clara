import config
from OllamaClient import OllamaClient
from DiscordClient import ClaraBot


if __name__ == "__main__":
    model = "gemma3"
    persona = config.get_persona("persona.txt")
    discord_api_key = config.get_key("keys.json", "discord")

    ai = OllamaClient("OLLAMA_HOST", model)
    ai.set_persona(persona)

    bot = ClaraBot(ai, prefix="!")
    bot.run(discord_api_key)
