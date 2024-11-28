import discord

from discord import ButtonStyle


class CollageView(discord.ui.View):
    def __init__(self, client, user):
        super().__init__(timeout=None)
        self.client = client
        self.user = user

    @discord.ui.button(label='Delete', custom_id='button-delete', style=ButtonStyle.danger)
    async def delete(self, interaction, button):
        if interaction.user == self.user:
            await interaction.message.delete()
        else:
            await interaction.response.send_message("You can only delete your own message.", ephemeral=True)
