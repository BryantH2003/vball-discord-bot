import discord
from discord.ext import commands, tasks
import os
import webserver
from oauth2client.service_account import ServiceAccountCredentials
from spreadSheetData import get_sheet_data
from embedMsg import build_embed_from_data
from cacheFile import load_message_cache, save_message_cache

DISCORD_TOKEN = os.environ['discordkey']

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.messages = True
client = commands.Bot(command_prefix = '!', intents=intents)

message_cache = load_message_cache()

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
        try:
            channel = client.get_channel(message_cache["channel_id"])
            message = await channel.fetch_message(message_cache["message_id"])
            
            if reaction.message.id != message.id:
                return

            new_data = get_sheet_data()
            new_embed = build_embed_from_data(new_data)
            await message.edit(embed=new_embed)
            await reaction.remove(user)
            
        except Exception as e:
            print(f"Error refreshing message: {e}")


@client.event
async def on_raw_reaction_add(payload):
    global message_cache

    if payload.user_id == client.user.id:
        return

    if str(payload.emoji.name) == "🔁" and message_cache:
        try:
            if payload.message_id != message_cache["message_id"]:
                return

            channel = client.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            user = await client.fetch_user(payload.user_id)

            new_data = get_sheet_data()
            new_embed = build_embed_from_data(new_data)
            await message.edit(embed=new_embed)
            await message.remove_reaction("🔁", user)
        except Exception as e:
            print(f"Error in raw reaction refresh: {e}")

# Custom Bot Commands 
@client.command()
async def bitch(ctx):
    await ctx.send("Shut up you peasant")
    
@client.command()
async def who_is_the_worst_player(ctx):
    await ctx.send("I think the Newton is among the bottom of the barrel in this group.")
    
@client.command()
async def opengym(ctx, time, location, signupLink):
    global message_cache

    # Close the old message if it exists
    if message_cache:
        try:
            channel = client.get_channel(message_cache["channel_id"])
            old_message = await channel.fetch_message(message_cache["message_id"])
            await old_message.edit(content="**This session is now CLOSED.**", embed=None)
        except Exception as e:
            print(f"Error closing old message: {e}")

    # Post the new session
    data = get_sheet_data()
    embed = build_embed_from_data(data, time, location, signupLink)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("🔁")

    # Update the in-memory and saved cache
    message_cache = {
        "message_id": msg.id,
        "channel_id": ctx.channel.id,
        "user_id": ctx.author.id
    }
    
    save_message_cache(message_cache)

    
webserver.keep_alive()
client.run(DISCORD_TOKEN)