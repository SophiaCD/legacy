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

    """if message.content.lower().startswith("!"):
        value = int(message.content[4:])
        response = Roll(value)"""
    if message.content.lower().startswith("!"):
        #"!4+20-2"
        #"!-1-345+234+1445"
        sign = "+"
        messcon = 1
        response = ""
        rolls =[]

        """Check if there is a sign, if there is a sign 
        it moves the message forward 1 to account for the bonus text.
        If there is no sign, positive is assumed"""
        if message.content[messcon:] == "-":
            sign ="-"
            messcon=messcon+1
        elif message.content[messcon:] == "+":
            messcon=messcon+1
        
        NumOfDice=""
        runing = True
        while runing == True:
            if message.content[messcon:] == "+" or message.content[messcon:] == "-" or message.content[messcon:] == " ":
                runing = False
            else:
                NumOfDice = NumOfDice+message.content[messcon:]
                messcon = messcon+1

        NumOfDice = int(NumOfDice)
        for i in range(1,NumOfDice):
            return random.randint(1, 100)
        
        #Convert NumOfDice and sign into a number
            
        
        letters = []
        for letter in message.content:
            letters.append(letter)
    
        for i in range(1,letters.len):
            print(i)
    else:
        return

    await message.channel.send(response)
    


# functions below here...

def Roll(NumOfDice, sign):
    if sign == "-":
        for i in range(1,NumOfDice):
            print(i)
    return random.randint(1, dieNum)

def multiRoll(numOfdie, dieNum):
    num = 0
    for i in range(numOfdie):
        num = num + random.randint(1, dieNum)
    return num





#message.author.name == "charliecat"
client.run(TOKEN)
