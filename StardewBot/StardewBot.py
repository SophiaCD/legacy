# bot.py
#textFile = "stardewBotText.txt"
textFile = "stardewBotText-20211106-1308.txt"
import os
import random
import re
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
NUMS = [":one:",":two:",":three:",":four:",":five:",":six:",":seven:",":eight:",":nine:"]
TOKENS = [":o:",":x:"]
#TURNS = []
#PLAYERS = ["",""]
#TTT = NUMS
TTTGAME = {
    'board': None,
    'turns': [],
    'players': ["",""],
    'grid': [":one:",":two:",":three:",":four:",":five:",":six:",":seven:",":eight:",":nine:"],
    'winner': ""
    }
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
    response = False
    if message.author == client.user:
        return
    elif message.content.lower() == "sv":
        print('manual')
        response = ""
        f = open("stardewBotUserManual.txt",'rt')
        lines = f.readlines()
        f.close()
        for i in range(0,len(lines)):
            response = response+lines[i]
    elif message.content.lower().startswith("svc"):
        response = addCounter(message)
    elif message.content.lower().startswith("svs"):
        print('stop;')
        response = stopCounter(message)
    elif message.content.lower() == ("t"):
        response = readAndIncrement()
        
    elif message.content == "Hi" or message.content == "Hello":
        response = "Hello"
    elif message.content == "Bye":
        response = "Bye"
    else:
        return
    if response:
        response = f'{message.author.mention} :evergreen_tree: **Result:** {response}'
        if len(str(response)) >= 2000:
            response = response[0:990] + '    ...    ' + response[len(response)-990:]
        await message.channel.send(response)
    else:
        print(f'no response: "{message.content}" from {message.author.name}')
    
# functions below here...
def readAndIncrement():
    print('!')
    response =""
    text = ""
    lines = reads()
    #+week day info
    #Use days of the year %7 for the day of the week
    #Use one line plus “\n” for all of the things in a day
    #Should add a function to assign things to certain days of the week
    for i in range(0,len(lines)):
        print(i)
        line = lines[i]
        resultB = re.match('([a-zA-Z ]+)=([0-9]+)B([0-9]+)', line)
        result = re.match('([a-zA-Z ]+)=([0-9]+)', line)
        resultD = re.match('d([0-9]+)', line)
        if (resultB):
            print("Bounce!!!")
            print(line)
            name = resultB.group(1)
            time = int(resultB.group(2))-1
            bounce = int(resultB.group(3))
            line = f'{name}={time+1}'
            response += line + "\n"
            #fix,.,..,.,.,.,.,.,.,,.,..,.,.,.,.,..,.,.,.,.,..,.,.,,..,.,.,.,.,..,.,.,.,.,..,.,.,..,.,.,.,.,.,.,.,.,.,.,..,.,.,.
            if time < 0:
                print(f"time = bounce {time}={bounce}")
                time = bounce
                print(f"time = bounce {time}={bounce}")
                print(line)
            line = f"{name}={time}B{bounce}\n"
            text += line
            print(line)
        elif (result):
            print(line)
            name = result.group(1)
            time = int(result.group(2))-1
            line = f'{name}={time}\n'
            response += line
            if time>0:
                text += line
            print(line)
        elif (resultD):
            day = int(resultD.group(1))%112 + 1
            text += "d"+str(day)+"\n"
            #response = "Day "+str((day-1)%28+1)+" of " + findSeason(day) + "\n"
            response += f"Day {str((day-1)%28+1)} of {findSeason(day)}\n"
            response += weekInfo(day)
            #response time
        else:
            return "text file issue"
    overWrite(text)
    return response

#
def findSeason(day):
    Season = int((day-1)/28+1)
    print("day,Season")
    print(day)
    print(+Season)
    if Season<= 1:
       return "Spring"
    elif Season<= 2:
        return "Summer"
    elif Season<= 3:
        return "autumn"
    elif Season<= 4:
        return "winter"
    else:
        return "Season Error"


def weekInfo(day):
    weekday = (day-1)%7
    if weekday == 0:
        return "Monday\nMarnie's Ranch closed\ngifting\ngifting\n\n"
    elif weekday == 1:
        return "Tuesday\nexercise: Marnie's Ranch & Carpenter's Shop closed\n\n"
    elif weekday == 2:
        return "Wednesday\nPierre's General Store is closed\nThe Queen of Sauce\n\n"
    elif weekday == 3:
        return "Thursday\n\n"
    elif weekday == 4:
        return "Friday\nTraveling Cart\nIf the Community Center has been restored the Blacksmith is unavailable\n\n"
    elif weekday == 5:
        return "Saturday\nFish Shop is closed unless it is raining\n\n"
    elif weekday == 6:
        return "Sunday\nThe Desert Trader sells 1 Staircase for 1 Jade\nThe Queen of Sauce\ngifting\n\n"

def stopCounter(message):
    #Add selective deletion?
    print('stopCounter')
    response = "not found"
    text = ""
    result = re.match('svs ([a-zA-Z ]+)', message.content.lower())
    name =result.group(1)
    f = open(textFile,'rt')
    lines = f.readlines()
    f.close()
    for i in range(0,len(lines)):
        line = lines[i].lower()
        if line.lower().startswith(name):
            print(f'Found you {name}')
            response = "stoped counter"
        else:
            print(f'not you {line}')
            text = text + line
    overWrite(text)
    return response

    
def addCounter(message):
    print('!')
    resultBounce = re.match('svc ([a-zA-Z ]+) ([0-9]+)b([0-9]+)', message.content.lower())
    #resultP = re.match('SV ([a-zA-Z ])', message.content)
    if (resultBounce):
        print('!')
        print('resultBounce')
        print(resultBounce.group(0), resultBounce.group(1), resultBounce.group(2))
        name = resultBounce.group(1)
        time = int(resultBounce.group(2))-1
        bounce = int(resultBounce.group(3))-1
        if (int(time)> 0 and int(bounce)>1):
            Write(name + "=" + str(time) + "B" + str(bounce) + "\n")
            response = "added bounce"
        else:
            response = "Invalid bounce or number"
        return response

    resultSimple = re.match('svc ([a-zA-Z ]+)([0-9]+)', message.content.lower())
    if (resultSimple):
        print('!')
        print(resultSimple.group(0), resultSimple.group(1), resultSimple.group(2))
        name = resultSimple.group(1)
        time = int(resultSimple.group(2))-1
        if (int(resultSimple.group(2))> 0):
            Write(name + "=" + str(time) + "\n")
            response = "added"
        else:
            response = "Invalid number"
        return response

    resultLookup = re.match('svc ([a-zA-Z ]+)', message.content.lower())
    if (resultLookup):
        print('!')
        print(resultLookup.group(0), resultLookup.group(1))
        name = resultLookup.group(1)
        match = MatchAndAdd(name.lower())
        #match[0] = name
        #match[1] = time
        #match[2] = bounce
        if not match:
            response = "not found"
        elif len(match)>2:
            Write(match[0] + "=" + str(int(match[1])-1) + "B" + match[2] + "\n")
            response = "found bounce"
        else:
            Write(match[0] + "=" + str(int(match[1])-1) + "\n")
            response = "found counter"
    return response

def MatchAndAdd(name):
    match = []
    f = open("stardewBotTextPremade.txt",'rt')
    lines = f.readlines()
    f.close()
    for i in range(0,len(lines)):
        line = lines[i].lower()
        if line.startswith(name):
            
            result = re.match('[a-zA-Z ]+=([0-9]+)B([0-9]+)', line)
            print(line)
            if result:
                print('!')
                print(result.group(0), result.group(1), result.group(2))
                match.append(name)
                match.append(result.group(1))
                match.append(result.group(2))
                return match
            
            result = re.match('[a-zA-Z ]+=([0-9]+)', line)
            if result:
                print('!')
                print(result.group(0), result.group(1))
                match.append(name)
                match.append(result.group(1))
                return match
            print('no')
    return []

def ranWord():
    Num = roll(8)
    if Num == 1:
        return "bears "
    elif Num == 2:
        return "don’t "
    elif Num == 3:
        return "dig "
    elif Num == 4:
        return "on "
    elif Num == 5:
        return "dancing "
    elif Num == 6:
        return "They just don’t dig it "
    elif Num == 7:
        return ", "
    elif Num == 8:
        return ". "

def Write(Text):
    f = open(textFile,'a')
    f.write(str(Text))
    f.close()
    return
def reads():
    f = open(textFile,'rt')
    lines = f.readlines()
    f.close()
    return lines
def overWrite(text):
    f = open(textFile,'w')
    f.write(str(text))
    f.close()      

async def Counting(message):
    text = "Replace"
    if message:
        await message.edit(content= text)
    else:
        message = await message.channel.send(text)
    return "Done"



# keep this as the LAST command
client.run(TOKEN)
    
