from Patterns.ParamsMaker import *
from usefulClasses import FileLoader, RandomSingleton
import copy, stringManipulation

class FileWildCards(IPattern):
    def __init__(self):
        self.defaultParams = ParamsMaker(
            loops=(1, "n", "num"), 
            parameters=([], 'p', 'params'), 
            concatinator=(", ", "c", "concat")
        )
    
    def NormalizeParameters(self, extractedParams: list[str]) -> ParamsMaker:
        paramsDto = copy.deepcopy(self.defaultParams)
        for param in extractedParams:
            parts = param.split("=")
            if len(parts) == 2:
                if parts[1][:1] == "[":
                    parts[1] = ExtractBrackets(parts[1])
                paramsDto.UpdateParameter(parts[0], parts[1])
        return paramsDto
    
    def GetMatchedFiles(self, searched={}, blocked={}, pathMatches={}):
        containTags = False
        if len(searched) > 0 or len(blocked) > 0:
            containTags = True
        files = FileLoader().files
        filteredFiles = []
        
        for name, content in files.items():
            if len(pathMatches) < 1 or any(pathMatch.lower() in name.lower() for pathMatch in pathMatches):
                if content["type"] == "yaml":
                    if not content['value']:
                        continue
                    for wc, vars in content['value'].items():
                        tags = [tag.lower() for tag in vars['Tags']]
                        if all(item in tags for item in searched) and not any(item in tags for item in blocked):
                            vars["Prompt"] = wc
                            filteredFiles.append(vars)
                if not containTags:
                    lines = content["value"].split("\n")
                    for line in lines:
                        filteredFiles.append(line)
        return filteredFiles
    
    def GetInnerString(self, filteredFiles, settings: ParamsMaker):
        if len(filteredFiles) < 1:
            return ""
        
        selectedValues = RandomSingleton().choices(filteredFiles, k=int(settings.loops))
        returnString = ""
        first = True
        
        for selectedValue in selectedValues:
            if selectedValues is None:
                selectedValues = " "
            if isinstance(selectedValue, dict):
                params = {}
                if len(settings.parameters) > 0 and "Params" in selectedValue.keys():
                    i = 0
                    for paramName in selectedValue["Params"]:
                        if i > len(settings.parameters)-1:
                            break
                        params[paramName] = settings.parameters[i]
                        i += 1
                    for name, val in params.items():
                        selectedValue["Prompt"] = selectedValue["Prompt"].replace(f"#{name}", val)
                selectedValue = selectedValue["Prompt"]
            if not first:
                returnString += settings.concatinator
            returnString += selectedValue
            first = False
            
        return stringManipulation.ParseActions(returnString)
    
    def ParsePattern(self, str: str):
        parts = str.split(':')
        if len(parts) < 1:
            print("Empty Wildcard Detected")
            return ""
        
        tags = parts.pop(0)
        tags = ExtractBrackets(tags)
        settings = self.NormalizeParameters(parts)
        
        searched = [tag.lower() for tag in tags if not tag.startswith('--') and not tag.startswith('__')]
        blocked = [tag.lower()[2:] for tag in tags if tag.startswith('--')]
        pathMatches = [tag.lower()[2:-2] for tag in tags if tag.startswith('__')]

        filteredFiles = self.GetMatchedFiles(searched, blocked, pathMatches)
        return self.GetInnerString(filteredFiles, settings)
    
# fileWildCards = FileWildCards()
# params = fileWildCards.defaultParams

# print()
# print(f"Before update: loops={params.loops}, concat={params.concatinator}, parameters={params.parameters}")

# params.UpdateParameter("n", 5)
# params.UpdateParameter("c", "; ")
# params.UpdateParameter("p", {'key': 'value'})

# print(f"After update: loops={params.loops}, concat={params.concatinator}, parameters={params.parameters}")
