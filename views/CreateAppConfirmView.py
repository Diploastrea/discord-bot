import discord

from discord import ButtonStyle, PermissionOverwrite, File, Embed, Colour
from discord.utils import get
from PIL import Image
from io import BytesIO

from constants import RECRUITMENT_CATEGORY_ID, LEADERSHIP_ROLE_ID
from views.ApplicationView import ApplicationView


class CreateAppConfirmView(discord.ui.View):
    def __init__(self, client):
        super().__init__(timeout=None)
        self.client = client

    @discord.ui.button(label='Confirm', custom_id='azor:button-create-app-confirm', style=ButtonStyle.primary)
    async def confirm(self, interaction, button):
        guild = interaction.guild
        user = interaction.user
        recruit_category = get(guild.categories, id=RECRUITMENT_CATEGORY_ID)
        admin_role = guild.get_role(LEADERSHIP_ROLE_ID)

        overwrites = {
            guild.default_role: PermissionOverwrite(read_messages=False),
            guild.me: PermissionOverwrite(read_messages=True, send_messages=True),
            user: PermissionOverwrite(read_messages=True, send_messages=True),
            admin_role: PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
        }

        app_exists = f'{user.name}-application' in [app.name for app in recruit_category.channels[4:]]
        if not app_exists:
            await interaction.response.send_message("Your application has been created successfully.", ephemeral=True)
            channel = await guild.create_text_channel(f'{user.name} application', category=recruit_category,
                                                      overwrites=overwrites)
            message = f'{user.mention} Welcome! Please give yourself a short introduction and post screenshots of your ' \
                      'box (sorted by factions), pets, tree, collections and rank plates as shown in example collage ' \
                      'below. If you have a preference, please specify which guild branch you\'d like to join.'
            embed_message = f'If you pass the pre-requisites, admins will contact you for follow-up questions and give ' \
                            f'you further instructions on joining. We admins are not robots, but we will do our best to ' \
                            f'reply to you in a timely manner.'

            img = Image.open('images/collage.jpg')
            img_bytes = BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            file = File(img_bytes, 'summon.png')

            embed = Embed(description=embed_message, colour=Colour.dark_green())
            await channel.send(message, file=file, embed=embed, view=ApplicationView(self.client))
        else:
            await interaction.response.send_message(content='You can only create one application at a time.',
                                                    ephemeral=True)
