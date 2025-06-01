from discord.ext import commands
import os
import discord
import json
from datetime import datetime

UPLOAD_DIR = "data/uploads"
STORAGE_FILE = "data/storage.json"
MAX_FILE_SIZE = 8 * 1024 * 1024  # 8MB limit

class FileCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        self._init_storage()

    def _init_storage(self):
        if not os.path.exists(STORAGE_FILE):
            with open(STORAGE_FILE, 'w') as f:
                json.dump({"files": {}}, f)
        else:
            # Ensure the file has the expected structure
            data = self._load_storage()
            if "files" not in data:
                data["files"] = {}
                self._save_storage(data)

    def _load_storage(self):
        try:
            with open(STORAGE_FILE, 'r') as f:
                data = json.load(f)
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return {"files": {}}
        except Exception as e:
            print(f"Error loading storage file: {e}")
            return {"files": {}}

    def _save_storage(self, data):
        try:
            with open(STORAGE_FILE, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving storage file: {e}")

    @commands.command(name='add_file')
    async def add_file(self, ctx):
        """Upload a file to the bot's storage"""
        if not ctx.message.attachments:
            embed = discord.Embed(
                title="❌ Error",
                description="Please attach a file to upload!",
                color=discord.Color.red()
            )
            embed.add_field(
                name="How to use",
                value="1. Type `!add_file`\n2. Attach your file to the same message\n3. Send the message",
                inline=False
            )
            await ctx.send(embed=embed)
            return
            
        storage = self._load_storage()
        user_id = str(ctx.author.id)
        
        # Ensure user's file list exists
        if user_id not in storage.get("files", {}):
            storage["files"][user_id] = []
            
        for attachment in ctx.message.attachments:
            # Check file size
            if attachment.size > MAX_FILE_SIZE:
                await ctx.send(f"❌ File '{attachment.filename}' is too large! Maximum size is 8MB.")
                continue
                
            try:
                # Create a unique filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_filename = f"{user_id}_{timestamp}_{attachment.filename}"
                filepath = os.path.join(UPLOAD_DIR, safe_filename)
                
                # Save the file
                await attachment.save(filepath)
                
                # Store file information
                file_info = {
                    "filename": attachment.filename,
                    "size": attachment.size,
                    "url": attachment.url,
                    "uploaded_at": str(ctx.message.created_at),
                    "filepath": safe_filename
                }
                
                storage["files"][user_id].append(file_info)
                self._save_storage(storage)
                
                # Send success message
                embed = discord.Embed(
                    title="✅ File Uploaded Successfully",
                    description=f"File '{attachment.filename}' has been uploaded",
                    color=discord.Color.green()
                )
                embed.add_field(name="File Name", value=attachment.filename, inline=True)
                embed.add_field(name="File Size", value=f"{attachment.size/1024:.1f} KB", inline=True)
                embed.add_field(name="Download", value=f"[Click here]({attachment.url})", inline=True)
                embed.set_footer(text=f"Uploaded by {ctx.author.name}")
                await ctx.send(embed=embed)
                
            except Exception as e:
                await ctx.send(f"❌ Error uploading file '{attachment.filename}': {str(e)}")

    @commands.command(name='list_files')
    async def list_files(self, ctx):
        """List all files uploaded by the user"""
        storage = self._load_storage()
        user_id = str(ctx.author.id)
        
        # Check if user has any files
        if user_id not in storage.get("files", {}) or not storage["files"][user_id]:
            embed = discord.Embed(
                title="📁 No Files Found",
                description="You haven't uploaded any files yet!",
                color=discord.Color.orange()
            )
            embed.add_field(
                name="How to upload",
                value="1. Type `!add_file`\n2. Attach your file to the same message\n3. Send the message",
                inline=False
            )
            await ctx.send(embed=embed)
            return
            
        embed = discord.Embed(
            title="📁 Your Uploaded Files",
            description="Here are all the files you've uploaded:",
            color=discord.Color.blue()
        )
        
        files = storage["files"][user_id]
        for i, file_info in enumerate(files, 1):
            size_kb = file_info["size"] / 1024
            embed.add_field(
                name=f"{i}. {file_info['filename']}",
                value=(
                    f"Size: {size_kb:.1f} KB\n"
                    f"Uploaded: {file_info['uploaded_at']}\n"
                    f"[Download]({file_info['url']})"
                ),
                inline=False
            )
            
        embed.set_footer(text=f"Total Files: {len(files)} • Use !delete_file <number> to remove files")
        await ctx.send(embed=embed)

    @commands.command(name='delete_file')
    async def delete_file(self, ctx, index: int):
        """Delete an uploaded file using its index number"""
        storage = self._load_storage()
        user_id = str(ctx.author.id)

        # Check if user has any files
        if user_id not in storage.get("files", {}) or not storage["files"][user_id]:
            embed = discord.Embed(
                title="❌ Error",
                description="You don't have any files to delete!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        files = storage["files"][user_id]

        try:
            # Convert to 0-based index and validate
            index = int(index) - 1
            if index < 0 or index >= len(files):
                await ctx.send(f"❌ Invalid index! Please use a number between 1 and {len(files)}")
                return

            # Get file info and remove from storage data
            deleted_file_info = files.pop(index)
            self._save_storage(storage)

            # Delete file from filesystem
            filepath = os.path.join(UPLOAD_DIR, deleted_file_info["filepath"])
            if os.path.exists(filepath):
                os.remove(filepath)

            # Send success message
            embed = discord.Embed(
                title="✅ File Deleted",
                description=f"File '{deleted_file_info['filename']}' has been deleted.",
                color=discord.Color.green()
            )
            embed.set_footer(text=f"Deleted by {ctx.author.name}")
            await ctx.send(embed=embed)

        except ValueError:
            await ctx.send("❌ Invalid input! Please provide the number of the file you want to delete.")
        except Exception as e:
            await ctx.send(f"❌ Error deleting file: {str(e)}")
          