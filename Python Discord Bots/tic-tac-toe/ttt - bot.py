# bot.py
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
    if message.author == client.user:
        return
    #elif message.content.startswith("roll"):
    #    value = int(message.content[4:])
    #    response = roll(value)
        
    elif message.content == "Behold for I exist":
        response = "I look upon your existence with jealousy"
    elif message.content == "It’s learning":
        #response = "no I’m not"
        response = "... no I’m not"
        #response = "... no I’m not!"
        #response = "no, no I’m not"
        #response = "no I’m definitely not"
    elif message.content == "Roll58008d1":
        response = "I’m not writing boobs"
    elif message.content == "Roll69d1":
        response = "69(nice)"
    elif message.content == "Roll42069d1":
        response = "42069(nice)"

        
    elif message.content == "text":
        f = open("Text-Test.txt",'rt')
        response = f.read()
        f.close()
    elif message.content.lower() == "!help":
        f = open("User manual.txt",'rt')
        response = f.read()
        f.close()
    elif message.content == "AAA text":
        f = open("Text-Test.txt",'a')
        f.write("A")
        response = "DONE"
        f.close()

        
    elif message.content == "Hi" or message.content == "Hello":
        response = "Hello"
    elif message.content == "Bears":
        response = ranWord() + ranWord() + ranWord() + ranWord() + ranWord()

    elif message.content.lower().startswith("roll"):
        Write(message.content + " ")
        resultTwo = re.match('roll *([0-9]+)d([0-9]+)\+([0-9]+)', message.content)
        result = re.match('roll *([0-9]+)d([0-9]+)', message.content)
        #search('([0-9]+)d([0-9]+)', message.content)
        if (resultTwo):
            print(resultTwo.group(0), resultTwo.group(1), resultTwo.group(2), resultTwo.group(3))
            qty = int(resultTwo.group(1))
            die = int(resultTwo.group(2))
            Plus = int(resultTwo.group(3))
            response = multiRollPlus(qty, die, Plus)
        elif(result):
            print(result.group(0), result.group(1), result.group(2))
            qty = int(result.group(1))
            die = int(result.group(2))
            response = multiRoll(qty, die)
        Write(str(response) + "      ")
        #response = message(r'roll([0-9]+)d[0-9]+)')
        
    elif message.content == "Bye":
        response = "Bye"
    elif message.content == "TicTacTime":
        response = TicTacTime()
    elif message.content.lower().startswith("ttt"):
        #try:
        response = TicTac(int(message.content[3:]), message)
        board = TTTGAME['board']
        if board:
            await board.edit(content= response)
        else:
            TTTGAME['board'] = await message.channel.send(response)
        await message.delete()
        return
        #except:
        #   response = "Unable to TicTac"
    elif message.content == "TicTacToe":
        #response = "0, 0, 0\n 0, 0, 0\n 0, 0, 0"
        response = TicTacToe()
        
    elif message.content == "1-9":
        #response = "0, 0, 0\n 0, 0, 0\n 0, 0, 0"
        Counting(message)
        return
        
    elif message.content == "ng":
        ClearTTT()
        response = TicTacToe()
        TTTGAME['board'] = await message.channel.send(response)
        await message.delete()
        return
    else:
        return
    if response:
        if len(str(response)) >= 2000:
            response = response[0:990] + '    ...    ' + response[len(response)-990:]
        await message.channel.send(response)
    else:
        print(f'no response: "{message.content}" from {message.author.name}')
    
# functions below here...
def ClearTTT():
    for i in range(1,9):
        TTTGAME['grid'][i-1] = NUMS[i-1]
        print(TTTGAME['grid'][i-1])
        print(NUMS[i-1])
    while len(TTTGAME['turns']) > 0:
        TTTGAME['turns'].pop(0)
    for i in range(1,2):
        TTTGAME['players'][i-1] = ""
        
def multiRoll(quantity, dieNum):
    num = 0
    for x in range(0,quantity):
         num = num + random.randint(1, dieNum)
    return num
    
def multiRollPlus(quantity, dieNum,Plus):
    num = 0
    for x in range(0,quantity):
         num = num + random.randint(1, dieNum)
    return num+Plus
def roll(dieNum):
    return random.randint(1, dieNum)

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
    f = open("Text-Test.txt",'a')
    f.write(str(Text))
    f.close()
    return

def TicTacToe():
    TTT = TTTGAME['grid']
    message = ""
    for x in range(0,3):
        for y in range(0,3):
            message += TTT[3*x + y]
        message += '\n'
    #return TTT[0] + "," + TTT[1] + "," + TTT[2] + "\n" + TTT[3] + "," + TTT[4] + "," + TTT[5] + "\n" + TTT[6] + "," + TTT[7] + "," + TTT[8]
    return message


#message.author.name == "charliecat"
def TicTac(num, message):
    #winner = TTTGAME['winner']
    TTTGAME['winner']
    TTT = TTTGAME['grid']
    if TTTGAME['winner']== "":
        extra = ""
        if len(TTTGAME['turns']) == 0:
            TTTGAME['players'][0] = message.author.name
        isPlayer1 = message.author.name == TTTGAME['players'][0]
            
        if len(TTTGAME['turns']) == 1 and not isPlayer1:
            TTTGAME['players'][1] = message.author.name
        isPlayer2 = message.author.name == TTTGAME['players'][1]

        isCharlie = message.author.name == "charliecat"
        isX = len(TTTGAME['turns'])%2 == 0

        try:
            if num==0 or num>9: raise
            if isX and (isCharlie or isPlayer1):
                if TTT[num - 1] == NUMS[num - 1]:
                    TTT[num - 1] = TOKENS[0]
                    TTTGAME['turns'].append(num)
                else:
                    extra = "A piece is already there"
            elif not isX and (isCharlie or isPlayer2):
                if TTT[num - 1] == NUMS[num - 1]:
                    TTT[num - 1] = TOKENS[1]
                    TTTGAME['turns'].append(num)
                else:
                    extra = "A piece is already there"
        except:
            return "Not a valid move"
        
        TTTGAME['winner'] = win()
        if TTTGAME['winner']:
            return TicTacToe() +TTTGAME['winner'] + " wins!!!"
        return TicTacToe() + extra
    else:
        return TicTacToe()+ TTTGAME['winner'] + " wins!!!"

#Bears 1 don’t 2 Digging 3 on 4 dancing 5 randomise 6. They just don’t dig it 7
def TicTacTime():
    time = ""
    for i in range(len(TTTGAME['turns'])):
        time = time + str(TTTGAME['turns'][i])
    return time
def win():
    TTT = TTTGAME['grid']
    if TTT[0] == TTT[1] and TTT[1] == TTT[2]:
        return str(TTT[0])
    elif TTT[3] == TTT[4] and TTT[4] == TTT[5]:
        return str(TTT[4])
    elif TTT[6] == TTT[7] and TTT[7] == TTT[8]:
        return str(TTT[7])
    elif TTT[0] == TTT[3] and TTT[3] == TTT[6]:
        return str(TTT[3])
    elif TTT[1] == TTT[4] and TTT[4] == TTT[7]:
        return str(TTT[4])
    elif TTT[2] == TTT[5] and TTT[5] == TTT[8]:
        return str(TTT[5])
    elif TTT[0] == TTT[4] and TTT[4] == TTT[8]:
        return str(TTT[4])
    elif TTT[2] == TTT[4] and TTT[4] == TTT[6]:
        return str(TTT[4])
    else:
        return ""
async def Counting(message):
    text = "Replace"
    if message:
        await message.edit(content= text)
    else:
        message = await message.channel.send(text)
    return "Done"



# keep this as the LAST command
client.run(TOKEN)
    
