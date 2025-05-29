import discord

from discord import ButtonStyle


class DeleteAppConfirmView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Confirm', custom_id='azor:button-delete-app-confirm', style=ButtonStyle.primary)
    async def confirm(self, interaction, button):
        await interaction.channel.delete()
        await interaction.response.defer()
