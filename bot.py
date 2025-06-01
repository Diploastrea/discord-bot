import os

import discord
from discord import Intents
from discord.ext import commands
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from constants import NIHILUM_GUILD_ID
from models.Member import Base
from views.collage_view import CollageView
from views.create_app_confirm_view import CreateAppConfirmView
from views.delete_app_confirm_view import DeleteAppConfirmView
from views.recruitment_view import RecruitmentView
from views.close_app_view import CloseAppView


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='/', intents=Intents.all(), description='Quack!')
        self.db_engine = None
        self.db_session = None

    async def setup_hook(self):
        await self.setup_database()

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and not filename.startswith('_'):
                cog = f"cogs.{filename[:-3]}"
                await self.load_extension(cog)

        self.add_view(CloseAppView())
        self.add_view(CollageView(self, None))
        self.add_view(DeleteAppConfirmView())
        self.add_view(RecruitmentView())
        self.add_view(CreateAppConfirmView())

    async def setup_database(self):
        self.db_engine = create_async_engine(os.getenv('DB_URL'), echo=True)
        self.db_session = async_sessionmaker(bind=self.db_engine, expire_on_commit=False)

        async with self.db_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def on_ready(self):
        await self.tree.sync(guild=discord.Object(id=NIHILUM_GUILD_ID))
        print(f'We have logged in as {self.user}')
