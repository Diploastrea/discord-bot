import discord
from discord.ext import commands
from discord import Embed, Colour

from constants import LEADERSHIP_ROLE_ID, RECRUITMENT_CHANNEL_ID
from utils import is_not_leadership
from views.recruitment_view import RecruitmentView


class SetupCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        command = message.content.split()
        if len(command) == 0:
            return

        if command[0] == '!setup' and len(command) == 1:
            if is_not_leadership(message.author.roles, LEADERSHIP_ROLE_ID):
                return

            title = 'Guild Applications'
            description = 'Welcome! To apply to the Nihilum Empire, please click the \'Apply\' button below!'
            embed = Embed(title=title, description=description, colour=Colour.dark_green())
            recruit_channel = self.bot.get_channel(RECRUITMENT_CHANNEL_ID)

            await recruit_channel.send(embed=embed, view=RecruitmentView())
            await message.delete()


async def setup(bot: commands.Bot):
    await bot.add_cog(SetupCog(bot))
