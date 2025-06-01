from discord.ext import commands
import discord
import asyncio

from config import DISCOED_TOKEN as TOKEN
from commands import file_commands, link_commands, help_command

print(f"Bot Token Loaded: {TOKEN}")

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

bot.remove_command('help')

async def setup():
    await bot.add_cog(help_command.HelpCommand(bot))
    await bot.add_cog(file_commands.FileCommands(bot))  
    await bot.add_cog(link_commands.LinkCommands(bot))  

@bot.event
async def on_ready():
    print(f"✅ Bot is ready! Logged in as {bot.user}")

async def main():
    await setup()
    await bot.start(TOKEN)

asyncio.run(main())
