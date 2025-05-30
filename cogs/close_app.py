import discord
from discord.ext import commands
from discord import Embed, Colour

from constants import RECRUITMENT_CATEGORY_ID
from views.close_app_view import CloseAppView


class CloseAppCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        command = message.content.split()

        if command[0] == '!close' and len(command) == 1:
            if message.channel.category_id != RECRUITMENT_CATEGORY_ID:
                return

            await message.delete()

            title = 'Closing application'
            embed = Embed(title=title, colour=Colour.dark_green())
            await message.channel.send(embed=embed, view=CloseAppView(self))


async def setup(bot: commands.Bot):
    await bot.add_cog(CloseAppCog(bot))
