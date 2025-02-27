import discord

from discord.client import Client

intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
import os
curDir = os.getcwd()
botkeyPath = input('Please input the full path to where the botkey text file is (excluding filename): ')
if botkeyPath == '':
    botkeyPath = curDir
botkeyFile = input('Please input the botkey text file name (including extension): ')
botkey = ''

os.chdir(botkeyPath)
file = open(botkeyFile, 'r')
botkey = file.read()
file.close()
os.chdir(curDir)
enableTestMode = True
testMode = input('Press enter without typing anything to disable testMode else type literally anything: ')
if testMode == '':
    enableTestMode = False
if testMode.strip().lower() == 'literally anything':
    print('Ha ha, very funny and definitely original.')

commands = ['!addUser', '!bull_suggestUser']

def constructMessage() -> str:
    finalMessage = 'The current list of users is:\n'

    from listMaker import getCurrentUsersList

    pos = 0
    try:
        for user in getCurrentUsersList():
            pos += 1
            if pos <= 10:
                finalMessage += f'`{user[1]}({user[0]}) | Reasons: "{user[2]}"`\n'
            if pos == 11:
                finalMessage += 'See the full list [here](https://vschar-official.com/bannedUsers/bannedUsers.json)'
    except:
        finalMessage = 'List is either down, or no users have been added!'

    return finalMessage

@client.event
async def on_ready():
    print('Listening to commands as ' + str(client.user))


def splitString(string:str) -> list[str]:
    return string.split(', ')

@client.event
async def on_message(message:discord.Message):
    from listMaker import addUser, suggestUser
    content = message.content
    author = message.author
    self = client.user
    isSelf = (author == self)
    owner = (author.id == 714247788715573310 or author.id == 300020084808744962)
    guild = message.guild

    if isSelf:
        return
    else:
        if guild.id == 991595497376714832 and enableTestMode:
            if owner:
                if content.startswith('!addUser'):
                    await message.channel.send('Testing mode is on: `The bot is currently unavailable while testing features.`')

            if content.startswith('!bull_suggestUser') or content == '!getUsers':
                    await message.channel.send('Testing mode is on: `The bot is currently unavailable while testing features.`')
            return
        if owner:
            if content.startswith('!addUser'):
                commandStr = content.replace('!addUser ', '')
                command = splitString(commandStr)

                try:
                    addUser(command[0], command[1], command[2])
                    await message.channel.send(f'Successfully added user `{command[1]}({command[0]}) for "{command[2]}"`')
                except Exception as e:
                    print(f'COULD NOT ADD USER "{str(e)}"')

        if content == '!getUsers':
            await message.channel.send(constructMessage())

        if content.startswith('!bull_suggestUser'):
            commandStr = content.replace('!bull_suggestUser ', '')
            command = splitString(commandStr)

            if command.__len__() > 3:
                print(command)
                print('Error processing command!')
                await message.channel.send('Too many arguments, expected "`userID`, `name`, `reason`"!')
                
            if command.__len__() == 3:
                await message.channel.send(suggestUser(command[0], command[1], command[2], author.id))

            if command.__len__() < 3:
                await message.channel.send('Too little arguments, expected "`userID`, `name`, `reason`"!')

client.run(botkey)