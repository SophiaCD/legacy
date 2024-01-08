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
        return
    elif message.content == "hi":
        response = "hi"
    else:
        return
    await message.channel.send(response)
    
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
    

def roll(dieNum):
    return random.randint(1, dieNum)

def TicTacToe():
    TTT = TTTGAME['grid']
    message = ""
    for x in range(0,3):
        for y in range(0,3):
            message += TTT[3*x + y]
        message += '\n'
    #return TTT[0] + "," + TTT[1] + "," + TTT[2] + "\n" + TTT[3] + "," + TTT[4] + "," + TTT[5] + "\n" + TTT[6] + "," + TTT[7] + "," + TTT[8]
    return message

#def placeConnect4(position, message):
#    if (int(position) < 10 and int(position) > 0)
    
        

def CreateBoard(x,y):
    output = [":one:",":two:",":three:",":four:",":five:",":six:",":seven:"]
    for i in range(1,x):
        output.append("\n")
        for i in range(1,y):
            output.append(":black_square_button:")
    return output
    
#message.author.name == "charliecat"
def TicTac(num, message):
    #winner = TTTGAME['winner']
    ###TTTGAME['winner']
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



def con4Place(message):
    placePos = int(message.content[10:])-1
        #no 0s
    connect4Board = CON4GAME['board']
    if placePos>-1 and placePos<7:
        if not connect4Board:
            connect4Board = CreateConnect4Board()
            CON4GAME['board'] = connect4Board
        connect4Board[placePos] = ":ballot_box_with_check:"
        response = ""
        print(connect4Board)
        for i in range(0,len(connect4Board)):
            print("!")
            response = response + connect4Board[i]
    else:
        response = "Not a valid move"
    return response



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

# keep this as the LAST command
client.run(TOKEN)
    
