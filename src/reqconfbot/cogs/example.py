from discord import ApplicationContext
from discord import Bot
from discord.ext.commands import Cog
from discord.ext.commands import slash_command


class Example(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command()
    async def hello(self, ctx: ApplicationContext):
        await ctx.respond("Hi, this is a slash command from a cog!")

    @slash_command()  # Not passing in guild_ids creates a global slash command.
    async def hi(self, ctx: ApplicationContext):
        await ctx.respond("Hi, this is a global slash command from a cog!")
