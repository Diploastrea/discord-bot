import discord

from discord import ButtonStyle


class ConfirmView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Confirm', custom_id='azor:button-confirm', style=ButtonStyle.primary)
    async def confirm(self, interaction, button):
        await interaction.channel.delete()
        await interaction.response.defer()

    @discord.ui.button(label='Cancel', custom_id='azor:button-cancel', style=ButtonStyle.danger)
    async def cancel(self, interaction, button):
        await interaction.message.delete()
        await interaction.response.defer()
