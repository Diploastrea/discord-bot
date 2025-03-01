import os
import random
from datetime import datetime

import cv2
import discord
import numpy as np
from deep_translator import GoogleTranslator
from discord import Colour, Embed, File, Intents
from discord.ext import commands
from PIL import Image
from io import BytesIO

from dotenv import load_dotenv
from allsummon import all_summon
from celhyposummon import celhypo_summon
from constants import COUNTING_CHANNEL_ID, LEADERSHIP_ROLE_ID, RECRUITMENT_CHANNEL_ID, RECRUITMENT_CATEGORY_ID
from factionsummon import faction_summon
from utils import create_collage, is_not_leadership, create_embed
from views.CollageView import CollageView
from views.ConfirmView import ConfirmView
from views.RecruitmentView import RecruitmentView
from views.ApplicationView import ApplicationView
from wokesummon import woke_summon

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

client = commands.Bot(command_prefix='/', intents=Intents.all(), description='Quack!')

langs_dict = GoogleTranslator().get_supported_languages(as_dict=True)
load_dotenv()
token = os.getenv('TOKEN')


@client.event
async def setup_hook():
    client.add_view(ApplicationView(client))
    client.add_view(CollageView(client, client.user))
    client.add_view(ConfirmView())
    client.add_view(RecruitmentView(client))


@client.event
async def on_ready():
    await client.user.edit(username='Azor\'s duck')
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

    if command[0] == '!stitch':
        if len(message.attachments) == 0:
            await message.delete()
            return

        title = 'Image stitch'
        images = []
        for attachment in message.attachments:
            content_type = attachment.content_type
            if content_type.endswith('jpeg') or content_type.endswith('png'):
                image_bytes = await attachment.read()
                image = np.frombuffer(image_bytes, np.uint8)
                image = cv2.imdecode(image, cv2.IMREAD_COLOR)
                images.append(image)

        collage = None
        text = ''
        if len(command) >= 2:
            if command[1].isnumeric():
                collage = create_collage(images, int(command[1]))
                if len(command) > 2:
                    text = ' '.join(command[2:])
            else:
                text = ' '.join(command[1:])
                collage = create_collage(images, 3)
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
        await message.channel.send(text, file=file, embed=embed, view=CollageView(client, message.author))

    if command[0].isnumeric() and len(command) == 1 and message.channel.id == COUNTING_CHANNEL_ID:
        next_num = int(command[0]) + 1
        if message.author.name == 'azorahai23':
            await message.channel.send(next_num)

    if command[0] == '!setup' and len(command) == 1:
        if is_not_leadership(message.author.roles, LEADERSHIP_ROLE_ID):
            return

        title = 'Guild Applications'
        description = 'Welcome! To apply to the Nihilum Empire, please click the \'Apply\' button below!'
        embed = Embed(title=title, description=description, colour=Colour.dark_green())
        recruit_channel = client.get_channel(RECRUITMENT_CHANNEL_ID)

        await recruit_channel.send(embed=embed, view=RecruitmentView(client))
        await message.delete()

    if command[0] == '!close' and len(command) == 1:
        if message.channel.category_id != RECRUITMENT_CATEGORY_ID:
            return

        await message.delete()

        title = 'Closing application...'
        embed = Embed(title=title, colour=Colour.dark_green())
        await message.channel.send(embed=embed, view=ApplicationView(client))


client.run(token)
