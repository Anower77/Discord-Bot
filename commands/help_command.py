from discord.ext import commands
import discord

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def help(self, ctx):
        embed = discord.Embed(
            title="🤖 Bot Command Guide",
            description="Here's a detailed guide on how to use all bot commands:",
            color=discord.Color.blue()
        )

        # File Commands Section
        embed.add_field(
            name="📄 File Commands",
            value=(
                "**!add_file**\n"
                "• Upload a file to the bot\n"
                "• Attach the file to your message\n"
                "• Example: `!add_file` (with file attached)\n\n"
                "**!list_files**\n"
                "• View all your uploaded files\n"
                "• Shows file size and upload date\n"
                "• Files are numbered for easy deletion\n"
                "• Example: `!list_files`\n\n"
                "**!delete_file**\n"
                "• Delete an uploaded file\n"
                "• Format: `!delete_file <number>`\n"
                "• Example: `!delete_file 1`\n"
                "• Use `!list_files` first to see file numbers"
            ),
            inline=False
        )

        # Link Commands Section
        embed.add_field(
            name="🔗 Link Commands",
            value=(
                "**!add_link**\n"
                "• Save a link in a category\n"
                "• Format: `!add_link <category> <url>`\n"
                "• Example: `!add_link CV https://example.com`\n\n"
                "**!my_links**\n"
                "• View all your saved links\n"
                "• Links are organized by category\n"
                "• Example: `!my_links`\n\n"
                "**!delete_link**\n"
                "• Remove a link from a category\n"
                "• Format: `!delete_link <category> <number>`\n"
                "• Example: `!delete_link CV 1`\n"
                "• Use `!my_links` first to see link numbers"
            ),
            inline=False
        )

        # Tips Section
        embed.add_field(
            name="💡 Tips",
            value=(
                "• Remember to attach files when using `!add_file`\n"
                "• Use `!list_files` and `!my_links` to get the numbers for deletion\n"
                "• Categories are case-insensitive\n"
                "• URLs must start with http:// or https://"
            ),
            inline=False
        )

        # Footer
        embed.set_footer(
            text="Need help? Contact the server administrator",
            icon_url="https://cdn.discordapp.com/emojis/1234567890.png"
        )

        await ctx.send(embed=embed)
