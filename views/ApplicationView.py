import discord

from discord import ButtonStyle, Colour, Embed

from views.ConfirmView import ConfirmView


class ApplicationView(discord.ui.View):
    def __init__(self, client):
        super().__init__(timeout=None)
        self.client = client

    @discord.ui.button(label='Close application', custom_id='azor:button-close', style=ButtonStyle.danger)
    async def close(self, interaction, button):
        app_channel = self.client.get_channel(interaction.channel.id)
        embed_message = 'Are you sure you want to close the application? This action will delete the channel and ' \
                        'cannot be reversed.'
        embed = Embed(description=embed_message, colour=Colour.dark_green())

        message = await app_channel.send(embed=embed)
        await message.edit(view=ConfirmView())
        await interaction.response.defer()
