# Clara

Clara is an AI-powered Discord bot designed to chat naturally with users. Built on the [Ollama](https://ollama.ai) AI platform, Clara can take on different personalities through customizable personas, making her adaptable to a wide range of communities.

## Features

- **Conversational AI**: Clara uses Ollama’s natural language processing to generate engaging, context-aware responses.
- **Custom Personas**: Shape Clara’s tone and behavior by editing a simple persona file.
- **Seamless Discord Integration**: Built with `discord.py`, Clara plugs easily into your server.
- **Smart Triggers**: Clara can respond when mentioned or when specific keywords are detected.

## Project Structure

- `app/main.py`: The main entry point.
- `app/DiscordClient.py`: Defines the `ClaraBot` class and handles Discord events.
- `app/OllamaClient.py`: Manages communication with Ollama’s AI platform.
- `app/config.py`: Loads config values and persona settings.
- `app/persona.txt`: Define Clara’s personality and style.
- `app/requirements.txt`: Python dependencies.

## Getting Started

### Requirements

- Python 3.8+
- A Discord bot token
- Access to the Ollama AI platform
- Docker (optional, for containerized deployment)

### Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/nonofare/Clara.git
   cd Clara
   ```
2. Install dependencies:
   ```bash
   pip install -r app/requirements.txt
   ```
3. Add your configuration:
   - Create a keys.json file in the app/ directory with your Discord bot token:
   ```json
   {
     "discord": "YOUR_DISCORD_BOT_TOKEN"
   }
   ```
4. Run Clara:
   ```bash
   python app/main.py
   ```

### Running with Docker

1. Build the Docker image:
   ```bash
   docker build -t clara-bot ./app
   ```
2. Run the container:
   ```bash
   docker run -d clara-bot
   ```

### Configuration

- Edit persona.txt to change Clara’s style and behavior.
