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

message_cache = {}

# Main On Start Method
@client.event
async def on_ready():
    print("Vball bot is online")
    # check_sheet.start()
    
@client.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    if str(reaction.emoji) == "🔁":
        msg_id = reaction.message.id

        if msg_id in message_cache:
            try:
                new_data = get_sheet_data()
                new_embed = build_embed_from_data(new_data)
                await reaction.message.edit(embed=new_embed)
                await reaction.remove(user)  # allow reuse
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
async def showdata(ctx):
    data = get_sheet_data()

    embedVar = build_embed_from_data(data)

    # Send the embed and add a 🔁 reaction
    msg = await ctx.send(embed=embedVar)
    await msg.add_reaction("🔁")

    # Track this message for refresh purposes
    message_cache[msg.id] = {
        "channel_id": ctx.channel.id,
        "user_id": ctx.author.id
    }
    
webserver.keep_alive()
client.run(DISCORD_TOKEN)