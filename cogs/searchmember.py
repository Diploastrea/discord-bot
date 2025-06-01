import discord
from discord.ext import commands
from discord import app_commands, Embed, Colour
from sqlalchemy import select

from constants import NIHILUM_GUILD_ID, LEADERSHIP_ROLE_ID
from models.Member import Member
from utils import is_not_leadership, format_member_list


class SearchMemberCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='searchmember', description='Searches for member\'s record by discord or in-game name.')
    @app_commands.describe(member='Search by discord name', ingame_name='Search by in-game name')
    async def add_member(self, interaction, member: discord.Member = None, ingame_name: str = ''):
        if is_not_leadership(interaction.user.roles, LEADERSHIP_ROLE_ID):
            embed = Embed(description='You do not have the rights manage guild members.', colour=Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if not member and not ingame_name:
            embed = Embed(description='Please select a user or provide in-game name.', colour=Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if member:
            async with self.bot.db_session() as session:
                result = await session.execute(select(Member).where(Member.discord_name == member.name))
                found_member = result.scalar_one_or_none()

                if found_member:
                    embed = Embed(description=f'{format_member_list([found_member])}',
                                  colour=Colour.dark_green())
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return
                else:
                    embed = Embed(description=f'No record found for ${member.name}.', colour=Colour.red())
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return
        else:
            async with self.bot.db_session() as session:
                result = await session.execute(select(Member).where(Member.ingame_name.like(f'%{ingame_name}%')))
                found_members = result.scalars().all()

                if len(found_members) > 0:
                    embed = Embed(description=f'{format_member_list(found_members)}',
                                  colour=Colour.dark_green())
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return
                else:
                    embed = Embed(description=f'No records found by in-game name \'{ingame_name}\'.',
                                  colour=Colour.red())
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return


async def setup(bot: commands.Bot):
    await bot.add_cog(SearchMemberCog(bot), guild=discord.Object(id=NIHILUM_GUILD_ID))
