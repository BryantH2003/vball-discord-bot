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
    
    embedVar = discord.Embed(title="Open Gym Session", description="Info on the upcoming open gym session.", color=discord.Color.green())
    
    embedVar.add_field(name="Time", value="TIME", inline=True)
    embedVar.add_field(name="Location", value="LOCATION", inline=True)
    
    embedVar.add_field(name="", value="", inline=False)
    
    approved = ""
    pending = ""
    denied = ""
    
    for row in data:
        if row['Verified'] == "Approved":
            approved += row['Name']
            approved += '\n'
        
        if row['Verified'] == "Pending":
            pending += row['Name']
            pending += '\n'
        
        if row['Verified'] == "Denied":
            denied += row['Name']
            denied += '\n'
            
    embedVar.add_field(name="Approved <:green_square:>", value=approved, inline=True)
    embedVar.add_field(name="Pending <:yellow_square:>", value=pending, inline=True)
    embedVar.add_field(name="Denied <:red_square:>", value=denied, inline=True)

    await ctx.channel.send(embed=embedVar)
    
    # msg = "**Sheet Data:**\n"
    # for row in data:
    #     msg += f"{row['Name'], row['Verified']}\n"
    # await ctx.send(msg)
    
# Time Based Events    
@tasks.loop(seconds=60)  # every 60 seconds
async def check_sheet():
    channel = client.get_channel(1399067333766680720)
    data = get_sheet_data()
    await channel.send(f"Latest data:\n{data}")
    
webserver.keep_alive()
client.run(DISCORD_TOKEN)