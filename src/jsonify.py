type JsonFile = dict[str, any]

varsList:JsonFile = {}

class Jsonify:
    def set(name:str, value):
        r'''Sets `name` as `value`'''
        varsList.__setitem__(name, value)

    def flushJson(path:str):
        r'''This writes all variables set by `set(name, value)`, then resets the list of variables.'''
        file = open(path, 'w')
        
        import json as PyJson

        json = PyJson.dumps(varsList, indent=8)
        file.write(json)
        file.close()
        
        varsList.clear()

    def stringifyList(path:str, varList:list[list]):
        r'''This converts a list of lists as follows:
        
        `[["variableName",value],["variableName2",value]]`'''

        file = open(path)

        jsonVars:JsonFile = {}
        for var in varList:
            jsonVars.__setitem__(str(var[0]), var[1])

        import json as PyJson

        json = PyJson.dumps(jsonVars, indent=8)
        file.write(json)
        file.close()