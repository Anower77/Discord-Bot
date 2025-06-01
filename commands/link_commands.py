from discord.ext import commands
import json
import os
import discord

DATA_FILE = "data/links.json"

class LinkCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        self._init_storage()

    def _init_storage(self):
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'w') as f:
                json.dump({"links": {}}, f)
        else:
            try:
                with open(DATA_FILE, 'r') as f:
                    data = json.load(f)
                if "links" not in data:
                    new_data = {"links": data}
                    with open(DATA_FILE, 'w') as f:
                        json.dump(new_data, f, indent=4)
            except:
                with open(DATA_FILE, 'w') as f:
                    json.dump({"links": {}}, f)

    def _load_data(self):
        try:
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                if "links" not in data:
                    return {"links": data}
                return data
        except:
            return {"links": {}}

    def _save_data(self, data):
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)

    @commands.command(name='add_link')
    async def add_link(self, ctx, category: str, url: str):
        """Add a link to a category"""
        if not url.startswith(('http://', 'https://')):
            await ctx.send("❌ Please provide a valid URL starting with http:// or https://")
            return

        data = self._load_data()
        user_id = str(ctx.author.id)

        if user_id not in data["links"]:
            data["links"][user_id] = {}

        if category not in data["links"][user_id]:
            data["links"][user_id][category] = []

        if url not in data["links"][user_id][category]:
            data["links"][user_id][category].append(url)
            self._save_data(data)
            await ctx.send(f"✅ Link added to category **{category}**: {url}")
        else:
            await ctx.send("❌ This link is already saved in this category!")

    @commands.command(name='my_links')
    async def my_links(self, ctx):
        """Show all links saved by the user"""
        data = self._load_data()
        user_id = str(ctx.author.id)

        if user_id not in data["links"] or not data["links"][user_id]:
            await ctx.send("❌ You haven't saved any links yet!")
            return

        embed = discord.Embed(
            title=f"📚 Links for {ctx.author.name}",
            description="Here are all your saved links:",
            color=discord.Color.green()
        )

        for category, links in data["links"][user_id].items():
            if links:
                links_text = "\n".join([f"• {link}" for link in links])
                embed.add_field(
                    name=category.upper(),
                    value=links_text,
                    inline=False
                )

        await ctx.send(embed=embed)

    @commands.command(name='delete_link')
    async def delete_link(self, ctx, category: str, url: str):
        """Delete a link from a category"""
        data = self._load_data()
        user_id = str(ctx.author.id)

        if user_id not in data["links"] or category not in data["links"][user_id]:
            await ctx.send("❌ Category not found!")
            return

        # Normalize and find matching URL
        found_url = next(
            (link for link in data["links"][user_id][category]
             if link.strip().rstrip('/') == url.strip().rstrip('/')),
            None
        )

        if not found_url:
            await ctx.send("❌ Link not found in this category!")
            return

        data["links"][user_id][category].remove(found_url)
        self._save_data(data)
        await ctx.send(f"✅ Link removed from category **{category}**")
