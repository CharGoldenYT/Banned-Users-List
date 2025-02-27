type UserJson = dict[str, any]
UserJson = {
    "suggestorID": 0, 
    "suggestions": [
            [
                '0',
                'N/A',
                'N/A'
            ]
        ]
}
import os



def getListOfJsons(folder:str) -> list[str]:


    curDir = os.getcwd()
    os.chdir(folder)
    filePaths:list[str] = []
    for file in os.listdir():
        if file.endswith('.json'):
            filePaths.append(file)

    os.chdir(curDir)
    return filePaths

def getJsons(folder:str) -> list[str]:
    jsons:list[str] = []

    curDir = os.getcwd()

    os.chdir(folder)

    for jsonFile in getListOfJsons(folder):
        file = open(jsonFile, 'r')
        jsons.append(file.read())
        file.close()

    os.chdir(curDir)
    return jsons


def parseJson(rawJson:str) -> UserJson:
    import json
    jsonFile = json.loads(rawJson)
    return {
        "suggestorID": jsonFile['suggestorID'],
        "suggestions": jsonFile['suggestions']
    }