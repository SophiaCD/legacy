# bot.py
import os
import random
import re
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
client = discord.Client()

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
        return)')
    else:
        return
    if response:
        if len(str(response)) >= 2000:
            response = response[0:990] + '    ...    ' + response[len(response)-990:]
        await message.channel.send(response)
    else:
        print(f'no response: "{message.content}" from {message.author.name}')
    
# functions below here...

def multiRollPlus(quantity, dieNum,Plus):
    num = 0
    for x in range(0,quantity):
         num = num + random.randint(1, dieNum)
    return num+Plus
def roll(dieNum):
    return random.randint(1, dieNum)
def 

def Write(Text):
    f = open("Text-Test.txt",'a')
    f.write(str(Text))
    f.close()
    return

