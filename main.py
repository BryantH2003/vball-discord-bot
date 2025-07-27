import discord
from discord.ext import commands
import os
import webserver

DISCORD_TOKEN = os.environ['discordkey']

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix = '!', intents=intents)

@client.event
async def on_ready():
    print("Vball bot is online")
    
@client.command()
async def bitch(ctx):
    await ctx.send("Shut up you peasant")
    
@client.command()
async def who_is_the_worst_player(ctx):
    await ctx.send("I think the Newton is among the bottom of the barrel in this group.")
    
webserver.keep_alive()
client.run(DISCORD_TOKEN)