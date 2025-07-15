import discord
from discord.ext import commands
from OllamaClient import OllamaClient
import asyncio


class ClaraBot(commands.Bot):
    def __init__(self, ai_client: OllamaClient, prefix: str, intents=None):
        self.__ai_client = ai_client
        self.__collected_data = {}
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

            if message.guild and message.guild.id in self.__collected_data:
                server_info = self.__collected_data[message.guild.id]
                server_info_str = (
                    f"Server Name: {server_info['name']}\n"
                    f"Text Channels: {', '.join(server_info['channels'])}\n"
                    f"Voice Channels: {', '.join(server_info['voice_channels'])}\n"
                    f"Roles: {', '.join(server_info['roles'])}\n"
                    f"Members: {', '.join([member['name'] for member in server_info['members']])}"
                )
                full_prompt += f"\nServer Info:\n{server_info_str}"

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

    async def fit(self, guild: discord.Guild):
        if guild.id in self.__collected_data:
            self.__collected_data[guild.id].clear()

        data = {
            "name": guild.name,
            "members": [
                {
                    "id": member.id,
                    "name": member.name,
                    "roles": [
                        role.name for role in member.roles if role.name != "@everyone"
                    ],
                }
                for member in guild.members
            ],
            "channels": [channel.name for channel in guild.text_channels],
            "voice_channels": [channel.name for channel in guild.voice_channels],
            "roles": [role.name for role in guild.roles if role.name != "@everyone"],
        }

        self.__collected_data[guild.id] = data


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

    @commands.command(name="fit")
    async def fit(self, ctx: commands.Context):
        if ctx.guild is None:
            await ctx.send("This command can only be used in a server.")
            return

        await self.__bot.fit(ctx.guild)
        await ctx.send("Clara knows this server better now!")
