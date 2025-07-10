import discord
from discord.ext import commands
from OllamaClient import OllamaClient
import asyncio


class ClaraBot(commands.Bot):
    def __init__(self, ai_client: OllamaClient, prefix: str, intents=None):
        self.__ai_client = ai_client
        if intents is None:
            intents = discord.Intents.default()
            intents.presences = True
            intents.members = True
            intents.message_content = True

        super().__init__(command_prefix=prefix, intents=intents)

    @property
    def ai_client(self):
        return self.__ai_client

    async def on_ready(self):
        print(f"Bot logged in as {self.user}")
        await self.add_cog(ClaraCommands(self))

    async def on_message(self, message):
        if message.author == self.user:
            return

        content = message.content

        if content.lower().startswith("clara"):
            prompt = content[5:].strip()
            await self.respond(message, prompt)
            return

        if self.user and self.user.mentioned_in(message):
            prompt = content.replace(self.user.mention, "").strip()
            await self.respond(message, prompt)
            return

        await self.process_commands(message)

    async def respond(self, message: discord.Message, prompt: str):
        try:
            user = f"[{message.author.name}#{message.author.discriminator}]"
            full_prompt = f"{user}: {prompt}" if prompt else f"{user} greeted me."

            async with message.channel.typing():
                response = await asyncio.wait_for(
                    asyncio.to_thread(self.ai_client.ask, full_prompt),
                    timeout=60.0,
                )

            await message.channel.send(response)

        except asyncio.TimeoutError:
            await message.channel.send("Timeout waiting for Clara response.")
        except Exception as e:
            await message.channel.send(f"Clara encountered an error: {str(e)}")
            print(f"Error generating Clara response: {e}")


class ClaraCommands(commands.Cog):
    def __init__(self, bot: ClaraBot):
        self.__bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        latency = round(self.__bot.latency * 1000)
        await ctx.send(f"Pong! Latency: {latency}ms")

    @commands.command(name="ask")
    async def ask(self, ctx: commands.Context, *, prompt: str = ""):
        await self.__bot.respond(ctx.message, prompt)
