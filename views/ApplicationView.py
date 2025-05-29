import discord

from discord import ButtonStyle, Colour, Embed

from views.DeleteAppConfirmView import DeleteAppConfirmView


class ApplicationView(discord.ui.View):
    def __init__(self, client):
        super().__init__(timeout=None)
        self.client = client

    @discord.ui.button(label='Close application', custom_id='azor:button-close', style=ButtonStyle.danger)
    async def close(self, interaction, button):
        embed_message = 'Are you sure you want to close the application? This action will delete the channel and ' \
                        'cannot be reversed.'
        embed = Embed(description=embed_message, colour=Colour.dark_green())

        await interaction.response.send_message(embed=embed, view=DeleteAppConfirmView(), ephemeral=True)
