import discord
from discord.ext import commands

from utils import create_embed
from wokesummon import woke_summon


class TimegazeCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.woke_pity = dict()
        self.wokes = {'athalia', 'baden', 'belinda', 'brutus', 'eugene', 'ezizh', 'gavus', 'lyca', 'maetria', 'safiya',
                      'shemira', 'solise', 'talene', 'thane'}

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        command = message.content.split()
        if len(command) == 0:
            return

        if command[0] == '!tg' and (len(command) == 2):
            command[1] = command[1].lower()
            if command[1] not in self.wokes:
                return

            images = woke_summon(self.woke_pity, message.author.name, command[1])
            text = f'Timegazed by {message.author.name}'
            file, embed = create_embed(images=images, title='Timegaze', text=text, message=message)
            await message.channel.send(file=file, embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(TimegazeCog(bot))
