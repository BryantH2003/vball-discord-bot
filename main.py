import discord
from discord.ext import commands
import os
import webserver

DISCORD_TOKEN = os.environ['discordkey']

client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print("Vball bot is online")
    
@client.command
async def hello(ctx):
    await ctx.send("Hello")
    
webserver.keep_alive()
client.run(DISCORD_TOKEN)