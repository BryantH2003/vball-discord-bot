import discord

def build_embed_from_data(data, time, location):
    embedVar = discord.Embed(title="Open Gym Session", description="", color=discord.Color.green())

    embedVar.add_field(name="Time", value=time, inline=True)
    embedVar.add_field(name="Location", value=location, inline=True)
    embedVar.add_field(name="", value="", inline=False)

    approved = ""
    pending = ""
    backedOut = ""

    approvedPlayers = 0
    for row in data:
        if row['Verified'] == "Approved":
            approved += row['Name'] + '\n'
            approvedPlayers += 1
        elif row['Verified'] == "Pending":
            pending += row['Name'] + '\n'
        elif row['Verified'] == "Backed Out":
            backedOut += row['Name'] + '\n'

    embedVar.add_field(name="Approved :green_square:", value=approved or "-", inline=True)
    embedVar.add_field(name="Pending :yellow_square:", value=pending or "-", inline=True)
    embedVar.add_field(name="Backed Out :red_square:", value=backedOut or "-", inline=True)

    headcount = f"{approvedPlayers}/12"
    embedVar.add_field(name=headcount, value="", inline=False)
    
    return embedVar
