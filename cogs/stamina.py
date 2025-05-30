import discord
from discord.ext import commands
from discord import Embed


class StaminaCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        command = message.content.split()

        if command[0] == "!stam" and len(command) == 2:
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
                embed = Embed(title=title, description=f'You have {hit} {hits} left. You can rewind {rewind} {times}.')
                embed.set_footer(text=f'Queried by {message.author.name}', icon_url=message.author.display_avatar.url)

            await message.channel.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(StaminaCog(bot))
