import discord
from discord.ext import commands, tasks
import os
import webserver
from oauth2client.service_account import ServiceAccountCredentials
from spreadSheetData import get_sheet_data

DISCORD_TOKEN = os.environ['discordkey']

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix = '!', intents=intents)

# Main On Start Method
@client.event
async def on_ready():
    print("Vball bot is online")
    # check_sheet.start()

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
    msg = "**Sheet Data:**\n"
    for row in data:
        msg += f"{row['Name'], row['Verified']}\n"
    await ctx.send(msg)
    
# Time Based Events    
@tasks.loop(seconds=60)  # every 60 seconds
async def check_sheet():
    channel = client.get_channel(1399067333766680720)
    data = get_sheet_data()
    await channel.send(f"Latest data:\n{data}")
    
webserver.keep_alive()
client.run(DISCORD_TOKEN)