from discord.ext import commands
from utils.data_utils import load_data, save_data

class LinkManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add_link(self, ctx, category, *, link):
        username = str(ctx.author.name)
        data = load_data()

        # Initialize user if not present
        if username not in data:
            data[username] = {
                "CV": [],
                "resume": [],
                "certificate": [],
                "social": {},
                "job_links": []
            }

        if category.lower() in ["linkedin", "facebook"]:
            data[username]["social"][category.capitalize()] = link
        elif category.lower() in data[username]:
            data[username][category.lower()].append(link)
        else:
            await ctx.send("❌ Invalid category.")
            return

        save_data(data)
        await ctx.send(f"✅ Link added under `{category}`.")

    @commands.command()
    async def my_links(self, ctx):
        username = str(ctx.author.name)
        data = load_data()

        if username not in data:
            await ctx.send("❌ No links found for you.")
            return

        user_data = data[username]
        msg = f"📎 **Links for {username}:**\n"

        for category, content in user_data.items():
            if isinstance(content, list) and content:
                msg += f"\n**{category.upper()}**:\n" + "\n".join(content)
            elif isinstance(content, dict) and content:
                msg += f"\n**{category.upper()}**:\n"
                for key, val in content.items():
                    msg += f"- {key}: {val}\n"

        await ctx.send(msg or "No data to show.")
