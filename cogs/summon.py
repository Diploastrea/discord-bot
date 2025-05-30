import discord
from discord.ext import commands

from allsummon import all_summon
from factionsummon import faction_summon
from utils import create_embed


class SummonCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.all_pity = dict()
        self.faction_pity = dict()
        self.factions = {'lb', 'lightbearer', 'mauler', 'wilder', 'gb', 'graveborn'}

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        command = message.content.split()

        if command[0] == '!summon':
            title = 'All summon'
            if len(command) == 1:
                images = all_summon(self.all_pity, message.author.name)
            elif len(command) == 2 and command[1] in self.factions:
                command[1] = command[1].lower()
                title = 'Faction summon'
                images = faction_summon(self.faction_pity, message.author.name, command[1])
            else:
                return

            text = f'Summoned by {message.author.name}'
            file, embed = create_embed(images=images, title=title, text=text, message=message)
            await message.channel.send(file=file, embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(SummonCog(bot))
