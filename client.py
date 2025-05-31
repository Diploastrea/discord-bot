import os

import aiomysql
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
        self.db_pool = None

    async def setup_hook(self):
        await self.setup_mysql_pool()

        await self.load_extension('cogs.translate')
        await self.load_extension('cogs.stamina')
        await self.load_extension('cogs.stitch')
        await self.load_extension('cogs.setup_recruitment')
        await self.load_extension('cogs.close_app')
        await self.load_extension('cogs.summon')
        await self.load_extension('cogs.stargaze')
        await self.load_extension('cogs.timegaze')

        self.add_view(CloseAppView())
        self.add_view(CollageView(self, None))
        self.add_view(DeleteAppConfirmView())
        self.add_view(RecruitmentView())
        self.add_view(CreateAppConfirmView())

    async def on_ready(self):
        await self.tree.sync(guild=discord.Object(id=NIHILUM_GUILD_ID))
        print(f'We have logged in as {self.user}')

    async def setup_mysql_pool(self):
        self.db_pool = await aiomysql.create_pool(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT")),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            db=os.getenv("DB_NAME"),
            autocommit=True,
            minsize=1,
            maxsize=3
        )
