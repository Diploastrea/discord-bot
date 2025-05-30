import discord
from discord import app_commands, Embed
from discord.ext import commands
from deep_translator import GoogleTranslator

from constants import NIHILUM_GUILD_ID


class TranslateCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.langs_dict = GoogleTranslator().get_supported_languages(as_dict=True)

    @app_commands.command(name='translate',
                          description='Translates provided text from one language to another. By default translates '
                                      'text to English.')
    @app_commands.describe(text='Text to be translated',
                           source='Source language (auto-detect by default)',
                           target='Target language (English by default)')
    async def translate(self, interaction, text: str, source: str = '', target: str = ''):
        source = source or 'auto'
        target = target or 'en'

        title = 'Translator'
        translated = GoogleTranslator(source=source, target=target).translate(text)

        embed = Embed(title=title, description=translated)
        embed.set_footer(text=f'Queried by {interaction.user.name}', icon_url=interaction.user.display_avatar.url)

        await interaction.response.send_message(embed=embed)

    @translate.autocomplete('source')
    async def source_autocomplete(self, interaction, current: str):
        choices = [app_commands.Choice(name=language, value=self.langs_dict.get(language))
                   for language in self.langs_dict.keys() if current.lower() in language]
        return choices[:25]

    @translate.autocomplete('target')
    async def source_autocomplete(self, interaction, current: str):
        choices = [app_commands.Choice(name=language, value=self.langs_dict.get(language))
                   for language in self.langs_dict.keys() if current.lower() in language]
        return choices[:25]


async def setup(bot: commands.Bot):
    await bot.add_cog(TranslateCog(bot), guild=discord.Object(id=NIHILUM_GUILD_ID))
