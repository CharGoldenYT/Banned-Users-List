import json as pyjson
from typedefs import UserList

def getCurrentUsersList() -> UserList:
    file = open('bannedUsers.json', 'r')
    usersJson = file.read()
    file.close()

    bannedUsers:list[list[str]] = pyjson.loads(usersJson)['bannedUsers']

    return bannedUsers

def addUser(userID:int, name:str, reason:str) -> str:
    from jsonify import Jsonify

    curUsers:list[list[str]] = []

    try:
        file = open('bannedUsers.json', 'r') # re-use old file cause fuck you.
        json = pyjson.loads(file.read())
        file.close()
        curUsers = json['bannedUsers']
    except Exception as e:
        print('No file exists yet, or the JSON is malformed!')

    print(curUsers)
    exists = False
    try:
        for user in curUsers:
            if user[0] == str(userID):
                exists = True
                return 'User is already added!'
                
        if not exists:
            curUsers.append([str(userID), name, reason])

            Jsonify.set("comment", 'Json file for your importing convenience! generate commands with the script at `vschar-official.com/bannedUsers/script.py`')
            Jsonify.set("bannedUsers", curUsers)
            Jsonify.flushJson('bannedUsers.json')
            return f'Added {name}({str(userID)})!'
    except:
        return f'Could not add {name}({str(userID)})!'

def newSuggestion(userID:int, name:str, reason:str, id:int) -> (str | None):
    from jsonify import Jsonify

    curSuggestions:list[list[str]] = []

    try:
        file = open(f'suggestions/suggestions_{id}.json', 'r')
        json = pyjson.loads(file.read())
        file.close()
        curSuggestions = json['suggestions']
    except Exception as e:
        print(f'No file exists yet, creating a new one! (the error was {str(e)})')

    exists = False
    try:
        for suggestion in curSuggestions:
            if suggestion[0] == str(userID).strip():
                exists = True
                suggestion[2] = suggestion[2]+ ' / ' + reason # Account for potential duplicate reports.
                suggestion[1] = name

        if not exists:
            curSuggestions.append([str(userID).strip(), name, reason])

        from datetime import datetime
        Jsonify.set("suggestorID", id)
        Jsonify.set("lastSuggestTimestamp", datetime.now().timestamp())
        Jsonify.set("suggestions", curSuggestions)

        Jsonify.flushJson(f'suggestions/suggestions_{id}.json')
    except Exception as e:
        print(f'Could not Jsonify! {str(e)}')
        return f'Could not add {name}({str(userID)})!'
    
    return f'Added {name}({str(userID)})!'

def checkSuggestorTimeStamps(id:int) -> bool:       
    return False


def banUser(user:int):
    print('Empty Function!')

def shouldTimeOutUser(id:int) -> bool:
    file = open(f'suggestions/suggestions_{id}.txt', 'r')
    try:
        file.read()
    except:
        file.close()
        return False
    
    suggestions = file.read().splitlines()
    startRange = 0
    stopRange = 0

    stopRange = suggestions.__len__()
    if suggestions.__len__() >= 10:
        startRange = suggestions.__len__() - 10
    timestamps:list[str] = []
    for i in range(startRange, stopRange):
        yuh = suggestions[i].split('|')
        timestamps.append(yuh[0])

    if timestamps.__len__() > 0:
        if timestamps[3] == timestamps[4]:
            if timestamps[8] == timestamps[9]:
                banUser(id)
                return True
                
    return False

def getTimeStamp(id:int) -> str:
    file = open(f'suggestions/suggestions_{id}.txt', 'r')
    fileSplit = file.read().splitlines()
    file.close()

    found = False
    for properties in fileSplit:
        if properties[0].startswith('<timestamp value='):
            found = True
            return properties[0].replace('<timestamp value="', '').replace('"/>', '')
    if not found:
        return 'ERROR GETTING TIMESTAMP.'


def suggestUser(userID:int, name:str, reason:str, suggestor:int) -> (str | None):
    import time as pyTime
    import math
    time = math.floor(pyTime.time())

    try:
        import os
        os.makedirs('suggestions', exist_ok=True)
    except OSError as e:
        print(f'Could not make dir! "{str(e)}"')

    if checkSuggestorTimeStamps(suggestor):
        print (f'suggestor `{suggestor} has an unusually high amount of requests in a given time period!`')
        if not shouldTimeOutUser(suggestor):
            return 'You have been sending requests too often! Please wait a little BEFORE sending another request.'
        else:
            return f'You have been timed out from making any requests until {getTimeStamp(suggestor)}'
    else:
        return newSuggestion(userID, name, reason, suggestor)