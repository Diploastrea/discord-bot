import discord
from discord import Intents
from discord.ext import commands

from constants import NIHILUM_GUILD_ID
from views.collage_view import CollageView
from views.create_app_confirm_view import CreateAppConfirmView
from views.delete_app_confirm_view import DeleteAppConfirmView
from views.recruitment_view import RecruitmentView
from views.close_app_view import CloseAppView


class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='/', intents=Intents.all(), description='Quack!')

    async def setup_hook(self):
        await self.load_extension('cogs.translate')
        await self.load_extension('cogs.stamina')
        await self.load_extension('cogs.stitch')
        await self.load_extension('cogs.setup_recruitment')
        await self.load_extension('cogs.close_app')
        await self.load_extension('cogs.summon')
        await self.load_extension('cogs.stargaze')
        await self.load_extension('cogs.timegaze')

        self.add_view(CloseAppView(self))
        self.add_view(CollageView(self, None))
        self.add_view(DeleteAppConfirmView())
        self.add_view(RecruitmentView(self))
        self.add_view(CreateAppConfirmView(self))

    async def on_ready(self):
        await self.tree.sync(guild=discord.Object(id=NIHILUM_GUILD_ID))
        print(f'We have logged in as {self.user}')
