import discord
import numpy as np
import cv2
from discord.ext import commands
from discord import Embed, File
from PIL import Image
from io import BytesIO
from datetime import datetime

from utils import create_collage
from views.collage_view import CollageView


class StitchCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        command = message.content.split()

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
            await message.channel.send(text, file=file, embed=embed, view=CollageView(self, message.author))


async def setup(bot: commands.Bot):
    await bot.add_cog(StitchCog(bot))
