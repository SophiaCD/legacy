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

def ResetGame():
    return {'state': 0, 'playersNeeded': 0, 'players': [], 'playersResponded': 0, 'mainChannelID':"", 'bid': [0, "", 0]}
#emptyPlayer = [0,0,True,0
#'bid': [Highest bid, highest bidder, Number of passes in a row]
game = ResetGame()
#game = {'state': 0, 'playersNeeded': 0, 'players': [], 'playersResponded': 0, 'mainChannelID':"", 'bid': [0, "", 0]}

#player0 = ["", -1,-1,True,-1,]
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
    global game
    response = ""
    ctx = message.channel
    if message.author == client.user:
        return
    if message.content.lower() == "A":
        response = "How did you do that??????"
    if message.content.lower() == "skullgame"and game['state'] == 0:
        game['state'] = 1
        game['mainChannelID'] = message.channel
        response = "How many will be playing?"

    elif game['state'] == 1:
        try:
            playerCount = int(message.content)
            response = "All players message 'join'"
            print(f"playerCount {playerCount}")
            game['playersNeeded'] = playerCount
            print(f"game['playersNeeded'] {game['playersNeeded']}")
            game['state'] = 2
        except:
            # not int so ignore
            return
    
    elif message.content.lower() == "join" and game['state'] == 2:
        isNewPlayer = True
        for i in range(len(game['players'])):
            if message.author.mention == game['players'][i]['mention']:
                isNewPlayer = False
        if isNewPlayer == True:
            response = f'{message.author.mention} has joined'
            #Make player hand
            #newPlayer = player0.copy()
            #newPlayer[0] = message.author.id
            newPlayer = {
                'mention': message.author.mention,
                'RosesAboveSkull': -1,
                'RosesInHand': 4,
                'CardsDrawn': 0,
                'HaveSkull': True,
                'BiddingNum': -1,
                'isWining': 0,
                'channel': 0
                }
            #Make player thread
            guild = message.guild
            author = message.author
            
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                guild.me: discord.PermissionOverwrite(view_channel=True),
                author: discord.PermissionOverwrite(view_channel=True),
            }
            
            channel = await guild.create_text_channel(f'x💀x-{message.author}', overwrites=overwrites)

            newPlayer['channel'] = channel.id
            game['players'].append(newPlayer)
            
            await channel.send("How many roses will you put on top of your skull?")
            print(f"players needed {game['playersNeeded']}")
            print(f"players {len(game['players'])}")
            if len(game['players']) == game['playersNeeded']:
                print("no players needed")
                response = response + "\n All players joined"
                game['state'] = 3

    elif game['state'] == 3:
        try:
            playerNum = whichPlayerChannel(message)
            
            #print(f"playerNum = {playerNum}")
            print(f"game['playersResponded'] = {game['playersResponded']}")
            print(f"game['playersNeeded'] = {game['playersNeeded']}")
            if playerNum >= 0 and int(message.content) >= 0 and game['players'][playerNum]['RosesAboveSkull'] == -1 and int(message.content) <= game['players'][playerNum]['RosesInHand']:
                game['players'][playerNum]['RosesAboveSkull'] = int(message.content)
                response = f'Anyone can draw {int(message.content)} rose(s) before hitting your skull'
                game['playersResponded'] = game['playersResponded']+1
                if game['playersNeeded'] == game['playersResponded']:
                    print(playerNum)
                    game['state'] = 4
                    game['playersResponded'] = 0
                    game['bid'][2] = 0
                    game['bid'][0] = 0
                    game['bid'][1] = ""
                    await game['mainChannelID'].send(f"everyone please place your bid")
            elif playerNum >= 0 and int(message.content) >= 0 and game['players'][playerNum]['RosesAboveSkull'] == -1 and int(message.content) < game['players'][playerNum]['RosesInHand']:
                response = f"You only have {game['players'][playerNum]['RosesInHand']} roses"
        except:
            print('Error setting skull')
    elif game['state'] == 4:
        try:
            if int(message.content) > game['bid'][0]:
                isPlayer = False
                isPlayer = areTheyAPlayer(message)
                print(isPlayer)
                if isPlayer == True:
                    game['bid'][2] = 0
                    game['bid'][0] = int(message.content)
                    game['bid'][1] = message.author.mention
                    print(f"{game['bid'][1]} is wining")
                    response = f"{game['bid'][1]} has the highest bid, If you cannot bid higher please type 'pass'"
        except:
            isPlayer = False
            isPlayer = areTheyAPlayer(message)
            if message.content.lower() == "pass" and isPlayer == True and game['bid'][1] != message.author.mention:
                print('pass')
                game['bid'][2] = game['bid'][2]+1
                if game['bid'][2] == len(game['players'])-1:
                    gardenText = gardenTextGenerator()
                    response = f"{game['bid'][1]} has won the bidding, The wining bid is {game['bid'][0]}\nplease select which garden you would like to draw from\n{gardenText}"
                    game['state'] = 5
    elif game['state'] == 5:
        print("elif game['state'] == 5:")
        try:
            #if message <= Number of options AND int(message.content)>0 AND message.author is the one who wind the biding
            intMessage = int(message.content)
            if intMessage-1 <= len(game['players']) and intMessage-1>-1 and message.author.mention == game['bid'][1]:

                print(f"game['players'][intMessage-1]['RosesInHand'] = {game['players'][intMessage-1]['RosesInHand']}")
                print(f"game['players'][intMessage-1]['CardsDrawn'] = {game['players'][intMessage-1]['CardsDrawn']}")
                
                if game['players'][intMessage-1]['RosesInHand']-game['players'][intMessage-1]['CardsDrawn']<=0:
                    #if they have no Cards
                    response = f"{game['players'][int(message.content)]['mention']} had no Cards"
                    print("had no Cards")
                    
                elif game['players'][intMessage-1]['RosesAboveSkull']-game['players'][intMessage-1]['CardsDrawn']>0:
                    game['players'][intMessage-1]['CardsDrawn'] = game['players'][intMessage-1]['CardsDrawn']+1
                    game['bid'][0] = game['bid'][0]-1
                    gardenText = gardenTextGenerator()
                    response = f":rose::rose::rose::rose:\n{game['players'][intMessage-1]['RosesAboveSkull']} had a rose, {game['bid'][1]} only needs to draw {game['bid'][0]} more rose\n{gardenText}\n:rose::rose::rose::rose:"
                    if game['bid'][0] == 0:
                        response = f":crown::crown::crown::crown:\n{game['players'][intMessage-1]['RosesAboveSkull']} had a rose, {game['bid'][1]} has won this round\n:crown::crown::crown::crown:"
                        game['state'] == 5
                        authorNum = whichPlayerAuthor(message)
                        game['players'][authorNum]['isWining'] = game['players'][authorNum]['isWining']+1
                        #Check if they win
                        if game['players'][authorNum]['isWining'] == 2:
                            response = f":crown::crown::crown::crown:\n{game['players'][intMessage-1]['RosesAboveSkull']} had a rose, {game['bid'][1]} has won this game\n:crown::crown::crown::crown:"
                            #end game
                            for i in range(len(game['players'])):
                                channel_id = game['players'][i]['channel']
                                channel = client.get_channel(channel_id)
                                if channel is not None:
                                    if channel.name.startswith("x💀x"):
                                        await channel.delete()
                            game = ResetGame()
                            #game = {'state': 0, 'playersNeeded': 0, 'players': [], 'playersResponded': 0, 'mainChannelID':"", 'bid': [0, "", 0]}
                        else:
                            await resetRoses()
                    print(f"had a rose, game['bid'][0] = {game['bid'][0]}")

                else:
                    # Skull!
                    response = f":skull::skull::skull::skull:\n{game['players'][int(message.content)-1]['RosesAboveSkull']} had a skull\n:skull::skull::skull::skull:"
                    authorNum = whichPlayerAuthor(message)
                    HaveSkull = game['players'][authorNum]['HaveSkull']
                    RosesInHand = game['players'][authorNum]['RosesInHand']
                    skullsEmojis = ":skull::skull::skull::skull:"
                    channel = client.get_channel(game['players'][authorNum]['channel'])
                    if RosesInHand>0 and HaveSkull == True:
                        LoserMessage = f"{skullsEmojis}\nPlease reply 'skull' to lose your skull or 'rose' to lose a rose\n{skullsEmojis}"
                        game['state'] = 6
                    elif RosesInHand ==0 and HaveSkull == True:
                        LoserMessage = f"{skullsEmojis}\nyou lose your skull\n{skullsEmojis})"
                        game['players'][authorNum]['HaveSkull'] = False
                        game['playersNeeded'] = game['playersNeeded']-1
                        await resetRoses()
                    elif RosesInHand>0 and HaveSkull == False:
                        LoserMessage = f"{skullsEmojis}\nyou lose a rose\n{skullsEmojis}"
                        game['players'][authorNum]['RosesInHand'] = game['players'][authorNum]['RosesInHand']-1
                        await resetRoses()
                    elif RosesInHand ==0 and HaveSkull == False:
                        LoserMessage = f"{skullsEmojis}\nYou have nothing left to lose\n{skullsEmojis})"
                        await resetRoses()
                    await channel.send(LoserMessage)
                    print("had a skull")
        except:
            print("not int so ignore")
            #not int so ignore
            #return
        print("!!!")
    if game['state'] == 6:
        skullsEmojis = ":skull::skull::skull::skull:"
        print(f"game['bid'][1] = {game['bid'][1]}")
        if game['bid'][1] == message.author.mention and message.content.lower() == "skull":
            authorNum = whichPlayerAuthor(message)
            response = f"{skullsEmojis}\nyou lose your skull\n{skullsEmojis}"
            game['players'][authorNum]['HaveSkull'] = False
            print("player loses a skull")
            game['playersNeeded'] = game['playersNeeded']-1
            await resetRoses()
        if game['bid'][1] == message.author.mention and message.content.lower() == "rose":
            authorNum = whichPlayerAuthor(message)
            response = f"{skullsEmojis}\nyou lose a rose\n{skullsEmojis}"
            game['players'][authorNum]['RosesInHand'] = game['players'][authorNum]['RosesInHand']-1
            print("player loses a rose")
            await resetRoses()
    #Players[all][Roses above skull] = -1
    elif message.content.lower() =="!quit":
        response = "Game ended"
        #foreach channel_id in players
        for i in range(len(game['players'])):
            channel_id = game['players'][i]['channel']
            channel = client.get_channel(channel_id)
            if channel is not None:
                if channel.name.startswith("x💀x-"):
                    await channel.delete()
        #clear game data
        game = ResetGame()
        #game = {'state': 0, 'playersNeeded': 0, 'players': [], 'playersResponded': 0, 'mainChannelID':"", 'bid': [0, "", 0]}
        #game['playersNeeded'] = 0
        #game['players'] = []
        #game = {'state': 0, 'playersNeeded': 0, 'players': []}
        
    print(f"game state = {game['state']}")
    if response:
        if len(str(response)) >= 2000:
            response = response[0:990] + '    ...    ' + response[len(response)-990:]
        await ctx.send(response)
        print(f"sending '{response}' to channel {ctx.id}")
    else:
        print(f'no response: "{message.content}" from {message.author.name}')
    
#Functions below
def Write(Text):
    f = open("Text-Test.txt",'a')
    f.write(str(Text))
    f.close()
    return
async def resetRoses():
    game['state'] = 3
    for i in range(len(game['players'])):
        if game['players'][i]['HaveSkull'] != False:
            print(game['players'][i]['mention'])
            channel = client.get_channel(game['players'][i]['channel'])
            game['players'][i]['RosesAboveSkull'] = -1
            game['players'][i]['CardsDrawn'] = 0
            await channel.send("How many roses will you put on top of your skull?")
        elif game['players'][i]['HaveSkull'] != False:
            game['players'][i]['RosesAboveSkull'] = game['players'][i]['RosesInHand']
def whichPlayerChannel(message):
    for i in range(len(game['players'])):
        if message.channel.id == game['players'][i]['channel']:
            return i
    return -1
def whichPlayerAuthor(message):
    for i in range(len(game['players'])):
        if message.author.mention == game['players'][i]['mention']:
            return i
    return -1
def gardenTextGenerator():
    gardenText = ""
    for i in range(len(game['players'])):
        if game['players'][i]['RosesInHand'] > 0 or game['players'][i]['HaveSkull'] != False:
            gardenSize = game['players'][i]['RosesInHand']-game['players'][i]['CardsDrawn']
            crowns = ""
            print(f"gardenSize '{gardenSize}'")
            if game['players'][i]['HaveSkull'] != False:
                gardenSize = gardenSize+1
            for a in range(game['players'][i]['isWining']):
                crowns = crowns + ":crown:"
            gardenText = gardenText+ f"\n{i+1}: {crowns}{game['players'][i]['mention']} has {gardenSize} cards in their garden"
            #Add crowns if winning
            print(f"gardenText '{gardenText}'")
    return gardenText
    #Edge case: what if nobody has any cards?
def areTheyAPlayer(message):
    isPlayer = False
    for i in range(len(game['players'])):
        if message.author.mention == game['players'][i]['mention']:
            isPlayer = True
    return isPlayer
async def makePlayers(message):
    return

#def gardenTextGenerator():
 #   gardenText = ""
  #  for i in range(len(game['players'])):
   #     if game['players'][i]['RosesInHand'] > 0 or game['players'][i]['HaveSkull'] != False:
    #        gardenSize = game['players'][i]['RosesInHand']
     #       print(f"gardenSize '{gardenSize}'")
      #      if game['players'][i]['HaveSkull'] != False:
       #         gardenSize = gardenSize+1
        #    gardenText = gardenText+ f"\n{i}: {game['players'][i]['mention']} has {gardenSize} cards in there garden"
         #   #Add crowns if winning
          #  print(f"gardenText '{gardenText}'")
    #return gardenText
    #Edge case: what if nobody has any cards?

#keep this as the last command
client.run(TOKEN)
    
