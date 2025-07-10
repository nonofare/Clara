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


class ClaraCommands(commands.Cog):
    def __init__(self, bot: ClaraBot):
        self.__bot = bot

    @commands.command(name="clara")
    async def clara(self, ctx: commands.Context, *, message: str):
        try:
            user = f"[{ctx.author.name}#{ctx.author.discriminator}]"
            prompt = f"{user}: {message}"

            async with ctx.typing():
                response = await asyncio.wait_for(
                    asyncio.to_thread(self.__bot.ai_client.ask, prompt),
                    timeout=60.0,
                )

            await ctx.send(response)

        except asyncio.TimeoutError:
            await ctx.send("Timeout waiting for Clara response.")
        except Exception as e:
            await ctx.send(f"Error: {str(e)}")
            print(f"Error in 'clara' command: {e}")
