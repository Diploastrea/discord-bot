import discord
from discord.ext import commands
from discord import Embed, Colour, app_commands

from constants import RECRUITMENT_CATEGORY_ID, LEADERSHIP_ROLE_ID, NIHILUM_GUILD_ID, RECRUITMENT_CHANNEL_ID
from utils import is_not_leadership
from views.delete_app_confirm_view import DeleteAppConfirmView


class CloseAppCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='close',
                          description='Closes current application and deletes the channel.')
    async def close_app(self, interaction):
        if is_not_leadership(interaction.user.roles, LEADERSHIP_ROLE_ID):
            await self.send_error_message(
                interaction, 'You do not have the rights to close the application, please contact leadership.')
            return

        if interaction.channel.category_id != RECRUITMENT_CATEGORY_ID:
            await self.send_error_message(interaction, 'Command can only be used in recruitment category.')
            return

        if interaction.channel.category_id != RECRUITMENT_CATEGORY_ID:
            await self.send_error_message(interaction, 'Command can only be used in recruitment category.')
            return

        if interaction.channel.id == RECRUITMENT_CHANNEL_ID or '-application' not in interaction.channel.name:
            await self.send_error_message(interaction, 'Command can only be used in application channels.')
            return

        title = 'Closing application'
        embed_message = 'Are you sure you want to close the application? This action will delete the channel and ' \
                        'cannot be undone.'
        embed = Embed(title=title, description=embed_message, colour=Colour.red())

        await interaction.response.send_message(embed=embed, view=DeleteAppConfirmView(), ephemeral=True)

    @staticmethod
    async def send_error_message(interaction, error_message):
        embed = Embed(description=error_message, colour=Colour.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(CloseAppCog(bot), guild=discord.Object(id=NIHILUM_GUILD_ID))
