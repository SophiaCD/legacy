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
:\n - {members}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return)')
    if message.content.lower() == "skullgame":
        response = "skullgame"
    else:
        return
    if response:
        if len(str(response)) >= 2000:
            response = response[0:990] + '    ...    ' + response[len(response)-990:]
        await message.channel.send(response)
    else:
        print(f'no response: "{message.content}" from {message.author.name}')
    
# functions below here..

