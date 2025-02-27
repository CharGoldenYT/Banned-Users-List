import os
import time
import readJson

def stepPrint(step:str):
    print(f'Step: `{step}`')

print("Suggested to ban page generator v2 [Build 2]")
print('')
print('')
print('')
print('(C) CharGolden 2025')
print('')
time.sleep(0.5)

stepPrint('Variable Setup')

curDir = os.getcwd()
jsonDir = input(f'Where are the suggestion jsons located? (leave blank for `{curDir}/suggestions/`) ')
if jsonDir == '':
    jsonDir = curDir + '/suggestions/'

rawJsons:list[str] = []
finalHTML = '''<!DOCTYPE html>
<html>
    <head>
        <title>
            List of suggested to ban users!
        </title>
        <link rel="stylesheet" href="https://vschar-official.com/css/global-style.css">
    </head>

    <body>\n'''

stepPrint('Getting Json Files')

try:
    rawJsons = readJson.getJsons(jsonDir)
except Exception as e:
    print(f'Error getting jsons! `{str(e)}`')
    time.sleep(5)
    exit(1)

stepPrint('Compiling Webpage')

for jsonFile in rawJsons:
    json = readJson.parseJson(jsonFile)

    finalHTML += '        <div class="UserID_' + str(json['suggestorID']) + '">'

    users:list[list[str]] = json['suggestions']

    for user in users:
        finalHTML += ''' \n            userID: "''' + str(user[0]) + '''"<br>\n            name(at the time of suggestion): "''' + str(user[1]) + '''"<br>\n            reasons: "''' + str(user[2]).strip() + '''"<br>\n'''
    
    finalHTML += '        </div>\n'

finalHTML += '''    </body>
</html>'''

stepPrint('Writing to file.')
file = open('subindex.html', 'w'); file.write(finalHTML); file.close()

print('Closing in 5 seconds')
time.sleep(5)
exit(0)