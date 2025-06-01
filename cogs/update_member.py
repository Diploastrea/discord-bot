import discord
from discord.ext import commands
from discord import app_commands, Embed, Colour
from sqlalchemy import select

from constants import NIHILUM_GUILD_ID, LEADERSHIP_ROLE_ID
from models.Member import Member
from utils import is_not_leadership, member_exists


class UpdateMemberCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='updatemember', description='Updates member\'s in-game name or comment.')
    @app_commands.describe(member='Guild member to be updated',
                           ingame_name='Guild member\'s in-game name',
                           comment='Optional comment')
    async def add_member(self, interaction, member: discord.Member, ingame_name: str = '', comment: str = ''):
        if is_not_leadership(interaction.user.roles, LEADERSHIP_ROLE_ID):
            embed = Embed(description='You do not have the rights manage guild members.', colour=Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if not await member_exists(self.bot, member.name):
            embed = Embed(description=f'No record found for ${member.name}, please use add command first.',
                          colour=Colour.red())
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        async with self.bot.db_session() as session:
            async with session.begin():
                result = await session.execute(select(Member).where(Member.discord_name == member.name))
                existing_member = result.scalar_one_or_none()
                if ingame_name:
                    existing_member.ingame_name = ingame_name

                if comment:
                    existing_member.comment = comment

        embed = Embed(description=f'Successfully updated {existing_member.discord_name}\'s record!\n'
                                  f'> **In-game name:** {existing_member.ingame_name}\n'
                                  f'> **Comment:** {existing_member.comment}',
                      colour=Colour.dark_green())
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(UpdateMemberCog(bot), guild=discord.Object(id=NIHILUM_GUILD_ID))
