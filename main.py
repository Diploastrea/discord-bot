import os
import random
from datetime import datetime

import cv2
import discord
import numpy as np
from deep_translator import GoogleTranslator
from discord import Colour, Embed, File, Intents, ButtonStyle, PermissionOverwrite
from discord.ext import commands
from discord.utils import get
from PIL import Image
from io import BytesIO

from dotenv import load_dotenv
from allsummon import all_summon
from celhyposummon import celhypo_summon
from factionsummon import faction_summon
from utils import create_collage, is_not_leadership, create_embed
from wokesummon import woke_summon

COUNTING_CHANNEL_ID = 1227777390340739142
LEADERSHIP_ROLE_ID = 1151356225859092510
# 1238970123814178977 tavern
# 1151356225859092510 nihi
RECRUITMENT_CHANNEL_ID = 850621029109071872
# 1238958205057630350 tavern
# 850621029109071872 nihi
RECRUITMENT_CATEGORY_ID = 1238168650901487646
# 1238887499770761237 tavern
# 1238168650901487646 nihi

client = commands.Bot(command_prefix='!', intents=Intents.all())
langs_dict = GoogleTranslator().get_supported_languages(as_dict=True)

load_dotenv()
token = os.getenv('TOKEN')

all_pity = dict()
faction_pity = dict()
woke_pity = dict()
celhypo_pity = dict()
factions = {'lb', 'lightbearer', 'mauler', 'wilder', 'gb', 'graveborn'}
wokes = {'athalia', 'baden', 'belinda', 'brutus', 'eugene', 'ezizh', 'gavus', 'lyca', 'maetria', 'safiya', 'shemira',
         'solise', 'talene', 'thane'}
celhypos = {'athalia', 'twins', 'orthros', 'talene', 'wukong', 'flora', 'zaphrael', 'alna', 'morael', 'titus', 'haelus',
            'audrae', 'tarnos', 'veithael', 'daemia', 'liberta', 'malkrie', 'ezizh', 'mehira', 'zolrath', 'khazard',
            'mezoth', 'lucretia', 'mortas', 'leofric', 'zikis', 'framton', 'vyloris', 'cruke', 'olgath', 'lucilla',
            'lavatune'}

messages = ['It\'s your lucky day {}-chan! I\'ve come to help with your counting ♡UωU♡',
            'Roses are red, violets are blue, I\'m here to count with you {}-senpai!',
            'Hey there, {}-san! Let\'s do some math together and make Pythagoras-senpai proud!']


class ConfirmView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label='Confirm', custom_id='button-confirm', style=ButtonStyle.primary)
    async def confirm(self, interaction, button):
        await interaction.channel.delete()
        await interaction.response.defer()

    @discord.ui.button(label='Cancel', custom_id='button-cancel', style=ButtonStyle.danger)
    async def cancel(self, interaction, button):
        await interaction.message.delete()
        await interaction.response.defer()


class ApplicationView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label='Close application', custom_id='button-close', style=ButtonStyle.danger)
    async def close(self, interaction, button):
        await interaction.response.defer()
        app_channel = client.get_channel(interaction.channel.id)
        embed_message = 'Are you sure you want to close the application? This action will delete the channel and ' \
                        'cannot be reversed.'
        embed = Embed(description=embed_message, colour=Colour.dark_green())

        message = await app_channel.send(embed=embed)
        await message.edit(view=ConfirmView())


class RecruitmentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label='Apply', custom_id='button-apply', style=ButtonStyle.success,
                       emoji='<:poggers:1099095698688987177>')
    async def apply(self, interaction, button):
        guild = interaction.guild
        user = interaction.user
        recruit_category = get(guild.categories, id=RECRUITMENT_CATEGORY_ID)
        admin_role = guild.get_role(LEADERSHIP_ROLE_ID)

        overwrites = {
            guild.default_role: PermissionOverwrite(read_messages=False),
            guild.me: PermissionOverwrite(read_messages=True, send_messages=True),
            user: PermissionOverwrite(read_messages=True, send_messages=True),
            admin_role: PermissionOverwrite(read_messages=True, send_messages=True)
        }
        await interaction.response.defer()
        channel = await guild.create_text_channel(f'{user.display_name} application', category=recruit_category,
                                                  overwrites=overwrites)

        message = f'{user.mention} Welcome! Please give yourself a short introduction and post screenshots of your ' \
                  f'box (sorted by factions), pets, tree, and rank plates.'
        embed_message = f'If you pass the pre-requisites, admins will contact you for follow-up questions and give ' \
                        f'you further instructions on joining. We admins are not robots, but we will do our best to ' \
                        f'reply to you in a timely manner.'
        embed = Embed(description=embed_message, colour=Colour.dark_green())
        message = await channel.send(message, embed=embed)
        await message.edit(view=ApplicationView())


@client.event
async def on_ready():
    client.add_view(RecruitmentView())
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    command = message.content.split(' ')
    if command[0] == '!sg' and (len(command) == 2):
        command[1] = command[1].lower()
        if command[1] not in celhypos:
            return

        images = celhypo_summon(celhypo_pity, message.author.name, command[1])
        text = f'Stargazed by {message.author.name}'
        file, embed = create_embed(images=images, title='Stargaze', text=text, message=message)
        await message.channel.send(file=file, embed=embed)

    if command[0] == '!summon':
        title = 'All summon'
        if len(command) == 1:
            images = all_summon(all_pity, message.author.name)
        elif len(command) == 2 and command[1] in factions:
            command[1] = command[1].lower()
            title = 'Faction summon'
            images = faction_summon(faction_pity, message.author.name, command[1])
        else:
            return

        text = f'Summoned by {message.author.name}'
        file, embed = create_embed(images=images, title=title, text=text, message=message)
        await message.channel.send(file=file, embed=embed)

    if command[0] == '!tg' and (len(command) == 2):
        command[1] = command[1].lower()
        if command[1] not in wokes:
            return

        images = woke_summon(woke_pity, message.author.name, command[1])
        text = f'Timegazed by {message.author.name}'
        file, embed = create_embed(images=images, title='Timegaze', text=text, message=message)
        await message.channel.send(file=file, embed=embed)

    if command[0] == '!stam' and (len(command) == 2):
        title = 'Hit calculator'
        stam_count = command[1]
        if not stam_count.isnumeric():
            embed = Embed(title=title, description='Not a number!')
        else:
            stam_count = int(stam_count)
            hit = stam_count // 48
            rewind = (stam_count % 48) // 4
            hits = 'hit' if hit == 1 else 'hits'
            times = 'time' if rewind == 1 else 'times'
            embed = Embed(title=title,
                          description=f'You have {hit} {hits} left. You can rewind {rewind} {times}.')
            embed.set_footer(text=f'Queried by {message.author.name}', icon_url=message.author.display_avatar.url)

        await message.channel.send(embed=embed)

    if command[0] == '!translate':
        title = 'Translator'
        msg = message.content.split(' ', 1)[1]
        source = 'auto'
        target = 'en'

        if (command[1] in langs_dict or command[1] in langs_dict.values()) and (
                command[2] in langs_dict or command[2] in langs_dict.values()):
            source = command[1]
            target = command[2]
            msg = message.content.split(' ', 3)[3]

        translated = GoogleTranslator(source=source, target=target).translate(msg)

        embed = Embed(title=title, description=translated)
        embed.set_footer(text=f'Queried by {message.author.name}', icon_url=message.author.display_avatar.url)

        await message.channel.send(embed=embed)

    if command[0] == '!stitch' and len(command) <= 2:
        title = 'Image stitch'

        images = []
        for attachment in message.attachments:
            content_type = attachment.content_type
            if content_type.endswith('jpeg') or content_type.endswith('png'):
                image_bytes = await attachment.read()
                image = np.frombuffer(image_bytes, np.uint8)
                image = cv2.imdecode(image, cv2.IMREAD_COLOR)
                images.append(image)

        if len(images) == 0:
            await message.delete()
            return

        if len(command) == 2 and command[1].isnumeric():
            collage = create_collage(images, int(command[1]))
        else:
            collage = create_collage(images, 3)
        collage = cv2.cvtColor(collage, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(collage)

        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        current_timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f'stitch-{current_timestamp}.png'
        file = File(img_bytes, filename)

        embed = Embed(title=title)
        embed.set_image(url=f'attachment://{filename}')
        embed.set_footer(text=f'Queried by {message.author.name}', icon_url=message.author.display_avatar.url)

        await message.delete()
        await message.channel.send(file=file, embed=embed)

    if command[0].isnumeric() and len(command) == 1 and message.channel.id == COUNTING_CHANNEL_ID:
        next_num = int(command[0]) + 1
        if message.author.name == 'azorahai23':
            await message.channel.send(next_num)
        elif random.randint(1, 50) == 1:
            name = message.author.display_name
            title = str(random.choice(messages)).format(name)
            embed = Embed(title=title, description=next_num)
            embed.set_footer(text=f'Queried by {message.author.name}', icon_url=message.author.display_avatar.url)

            await message.channel.send(embed=embed)

    if command[0] == '!setup' and len(command) == 1:
        if is_not_leadership(message.author.roles, LEADERSHIP_ROLE_ID):
            return

        title = 'Guild Applications'
        description = 'Welcome! To apply to the Nihilum Empire, please click the \'Apply\' button below!'
        embed = Embed(title=title, description=description, colour=Colour.dark_green())

        recruit_channel = client.get_channel(RECRUITMENT_CHANNEL_ID)
        msg = await recruit_channel.send(embed=embed)

        await message.delete()
        await msg.edit(view=RecruitmentView())

    if command[0] == '!close' and len(command) == 1:
        if is_not_leadership(message.author.roles,
                             LEADERSHIP_ROLE_ID) or message.channel.category_id != RECRUITMENT_CATEGORY_ID:
            return

        await message.delete()

        title = 'Closing application...'
        embed = Embed(title=title, colour=Colour.dark_green())
        msg = await message.channel.send(embed=embed)
        await msg.edit(view=ApplicationView())


client.run(token)
