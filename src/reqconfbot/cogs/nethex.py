from discord import ApplicationContext
from discord import Bot
from discord.ext.commands import Cog
from discord.ext.commands import slash_command


class NethexCog(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command()
    async def nethex_cog_test(self, context: ApplicationContext):
        await context.respond("nethex_cog_test")
