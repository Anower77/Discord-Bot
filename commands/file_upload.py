import os
import discord
from discord.ext import commands

UPLOAD_DIR = "data/uploads"

class FileUpload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        os.makedirs(UPLOAD_DIR, exist_ok=True)

    @commands.command()
    async def upload_file(self, ctx):
        if ctx.message.attachments:
            for attachment in ctx.message.attachments:
                filepath = os.path.join(UPLOAD_DIR, attachment.filename)
                await attachment.save(filepath)
            await ctx.send("✅ File(s) saved successfully.")
        else:
            await ctx.send("❌ Please attach a file.")
