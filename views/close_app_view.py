import discord

from discord import ButtonStyle, Colour, Embed

from views.delete_app_confirm_view import DeleteAppConfirmView


class CloseAppView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Close application', custom_id='azor:button-close-app', style=ButtonStyle.danger)
    async def close_app(self, interaction, button):
        title = 'Closing application'
        embed_message = 'Are you sure you want to close the application? This action will delete the channel and ' \
                        'cannot be undone.'
        embed = Embed(title=title, description=embed_message, colour=Colour.red())

        await interaction.response.send_message(embed=embed, view=DeleteAppConfirmView(), ephemeral=True)
