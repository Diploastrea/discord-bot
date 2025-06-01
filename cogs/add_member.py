import discord
from discord.ext import commands
from discord import app_commands, Embed, Colour

from constants import NIHILUM_GUILD_ID, LEADERSHIP_ROLE_ID
from models.Member import Member
from utils import is_not_leadership, member_exists, format_member_list


class AddMemberCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='addmember', description='Adds a new guild member to the database.')
    @app_commands.describe(member='Guild member to be added',
                           ingame_name='Guild member\'s in-game name',
                           comment='Optional comment')
    async def add_member(self, interaction, member: discord.Member, ingame_name: str, comment: str = ''):
        if is_not_leadership(interaction.user.roles, LEADERSHIP_ROLE_ID):
            embed = Embed(description='You do not have the rights manage guild members.', colour=Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if await member_exists(self.bot, member.name):
            embed = Embed(description='A record already exists for selected member, please use update command instead.',
                          colour=Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        new_member = Member(member.name, ingame_name, comment)
        async with self.bot.db_session() as session:
            async with session.begin():
                session.add(new_member)

        embed = Embed(description='Added new guild member record to the database! <:poggers:1099095698688987177>\n'
                                  f'{format_member_list([new_member])}',
                      colour=Colour.dark_green())
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(AddMemberCog(bot), guild=discord.Object(id=NIHILUM_GUILD_ID))
