import disnake
from disnake.ext import commands

from client import Linguista
from config import datas


class Events(commands.Cog):
    def __init__(self, bot: Linguista):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(
            activity=disnake.Game(
                name=f"v{datas['BOT_VERSION']} | {len(self.bot.guilds):,} guilds."
            )
        )


def setup(bot):
    bot.add_cog(Events(bot))