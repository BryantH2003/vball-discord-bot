import discord
from discord.ext import commands, tasks
import os
import webserver
from oauth2client.service_account import ServiceAccountCredentials
from spreadSheetData import get_sheet_data
from embedMsg import build_embed_from_data

DISCORD_TOKEN = os.environ['discordkey']

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.messages = True
client = commands.Bot(command_prefix = '!', intents=intents)

message_cache = None

# Main On Start Method
@client.event
async def on_ready():
    print("Vball bot is online")
    # check_sheet.start()
    
@client.event
async def on_reaction_add(reaction, user):
    global message_cache

    if user.bot:
        return

    if str(reaction.emoji) == "🔁" and message_cache:
        if reaction.message.id == message_cache["message_id"]:
            try:
                new_data = get_sheet_data()
                new_embed = build_embed_from_data(new_data)
                await reaction.message.edit(embed=new_embed)
                await reaction.remove(user)
            except Exception as e:
                print(f"Error refreshing message: {e}")

# Custom Bot Commands 
@client.command()
async def bitch(ctx):
    await ctx.send("Shut up you peasant")
    
@client.command()
async def who_is_the_worst_player(ctx):
    await ctx.send("I think the Newton is among the bottom of the barrel in this group.")
    
@client.command()
async def opengym(ctx, time, location):
    global message_cache

    # Close previous message if it exists
    if message_cache:
        try:
            channel = client.get_channel(message_cache["channel_id"])
            old_message = await channel.fetch_message(message_cache["message_id"])
            await old_message.edit(content="**This session is now CLOSED.**", embed=None)
        except Exception as e:
            print(f"Error closing previous message: {e}")

    # Create new message
    data = get_sheet_data()
    embed = build_embed_from_data(data, time, location)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🔁")

    # Track this message
    message_cache = {
        "message_id": msg.id,
        "channel_id": ctx.channel.id,
        "user_id": ctx.author.id
    }

    
webserver.keep_alive()
client.run(DISCORD_TOKEN)