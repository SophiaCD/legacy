# bot.py
# secretly evil
import os
import random
import re
import discord
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

    #elif message.content.lower().startswith("ttt"):
    #    await message.delete()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    # members = '\n - '.join([member.name for member in guild.members])
    # print(f'Guild Members:\n - {members}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("roll"):
        print("1")
        value = int(message.content[4:])
        print("4")
        response = Roll(value)
    
    else:
        return

    await message.channel.send(response)
    
# functions below here...

def Roll(dieNum):
    return random.randint(1, dieNum)

def multiRoll(numOfdie, dieNum):
    num = 0
    for i in range(numOfdie):
        num = num + random.randint(1, dieNum)
    return num

#message.author.name == "charliecat"
client.run(TOKEN)
