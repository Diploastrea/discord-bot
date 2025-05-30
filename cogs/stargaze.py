import discord
from discord.ext import commands

from celhyposummon import celhypo_summon
from utils import create_embed


class StargazeCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.celhypo_pity = dict()
        self.celhypos = {'athalia', 'twins', 'orthros', 'talene', 'wukong', 'flora', 'zaphrael', 'alna', 'morael',
                         'titus', 'haelus', 'audrae', 'tarnos', 'veithael', 'daemia', 'liberta', 'malkrie', 'ezizh',
                         'mehira', 'zolrath', 'khazard', 'mezoth', 'lucretia', 'mortas', 'leofric', 'zikis', 'framton',
                         'vyloris', 'cruke', 'olgath', 'lucilla', 'lavatune'}

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        command = message.content.split()

        if command[0] == '!sg' and (len(command) == 2):
            command[1] = command[1].lower()
            if command[1] not in self.celhypos:
                return

            images = celhypo_summon(self.celhypo_pity, message.author.name, command[1])
            text = f'Stargazed by {message.author.name}'
            file, embed = create_embed(images=images, title='Stargaze', text=text, message=message)
            await message.channel.send(file=file, embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(StargazeCog(bot))
