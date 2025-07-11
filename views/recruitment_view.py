import discord


from discord import ButtonStyle, Embed, Colour

from views.create_app_confirm_view import CreateAppConfirmView


class RecruitmentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Apply', custom_id='azor:button-apply', style=ButtonStyle.success,
                       emoji='<:poggers:1099095698688987177>')
    async def apply(self, interaction, button):
        embed_message = 'Are you sure you want to create a new application? Please make sure to read the ' \
                        'requirements before applying.'
        embed = Embed(description=embed_message, colour=Colour.dark_green())

        await interaction.response.send_message(embed=embed, view=CreateAppConfirmView(), ephemeral=True)
