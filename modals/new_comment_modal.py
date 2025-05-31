import discord


class NewCommentModal(discord.ui.Modal):
    def __init__(self, bot):
        super().__init__(title="Submit a Comment")
        self.bot = bot

        self.ingame_name = discord.ui.TextInput(label="Applicant\'s ingame name", style=discord.TextStyle.short,
                                                required=True)
        self.comment = discord.ui.TextInput(label="Your comment", style=discord.TextStyle.paragraph, required=True)

    async def on_submit(self, interaction):
        # async with self.bot.db_pool.acquire() as conn:
        #     async with conn.cursor() as cursor:
        #         await cursor.execute(
        #             "INSERT INTO applications (discord_name, comment) VALUES (%s, %s)",
        #             (user.name, comment)
        #         )
        await interaction.response.send_message(f"Thanks! You submitted: {self.comment}", ephemeral=True)
