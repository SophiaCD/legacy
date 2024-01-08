
# This example requires the 'message_content' intent.
import os
import discord
import random
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('test'):
        await message.channel.send('Hello!')
    
    try:
        clean_str = list(message.content)
        bonus = 0
        operator = "+"
        for i in range(0, len(clean_str)):
            if clean_str[i] == "+":
                operator = "+"
            elif clean_str[i] == "-":
                operator = "-"
            else:
                if operator == "+":
                    bonus = bonus + int(clean_str[i])
                elif operator == "-":
                    bonus = bonus - int(clean_str[i])
        #bonus

        #roll
        rawroll = random.randint(1, 10)
        totRoll = rawroll+bonus
        #roll

        #strSuccess
        strSuccess = ""
        if totRoll < 2:
            strSuccess = "FAILURE AND!!!8"
        elif totRoll >1 and totRoll<5:
            strSuccess = "FAILURE"
        elif totRoll == 5:
            strSuccess = "FAILURE BUT"
        elif totRoll == 6:
            strSuccess = "SUCCESS BUT"
        elif totRoll >6 and totRoll<10:
            strSuccess = "SUCCESS"
        elif totRoll > 9:
            strSuccess = "SUCCESS AND!!!"
        #strSuccess
        
        response =  str(message.author) + ": " + strSuccess + "\n" + str(rawroll) +" + "+ str(bonus) + " = " + str(totRoll)
        print(response)
        await message.channel.send(response)
    except ValueError:
        print("not Valid")

client.run(TOKEN)
