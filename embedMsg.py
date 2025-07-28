import discord

def build_embed_from_data(data):
    embedVar = discord.Embed(title="Open Gym Session", description="", color=discord.Color.green())

    embedVar.add_field(name="Time", value="TIME", inline=True)
    embedVar.add_field(name="Location", value="LOCATION", inline=True)
    embedVar.add_field(name="", value="", inline=False)

    approved = ""
    pending = ""
    backedOut = ""

    for row in data:
        if row['Verified'] == "Approved":
            approved += row['Name'] + '\n'
        elif row['Verified'] == "Pending":
            pending += row['Name'] + '\n'
        elif row['Verified'] == "Backed Out":
            backedOut += row['Name'] + '\n'

    embedVar.add_field(name="Approved :green_square:", value=approved or "-", inline=True)
    embedVar.add_field(name="Pending :yellow_square:", value=pending or "-", inline=True)
    embedVar.add_field(name="Backed Out :red_square:", value=backedOut or "-", inline=True)

    return embedVar
