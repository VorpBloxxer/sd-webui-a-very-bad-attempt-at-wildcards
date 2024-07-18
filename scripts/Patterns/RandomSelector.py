from Patterns.ParamsMaker import *
from usefulClasses import FileLoader, RandomSingleton
import copy, stringManipulation
from collections import Counter

class RandomSelector(IPattern):
    def __init__(self):
        self.defaultParams = ParamsMaker(
            loops=("1", "n", "num"), 
            mode=("add", "m", "mod"), 
            concatinator=(", ", "c", "concat")
        )
    
    def NormalizeParameters(self, extractedParams: list[str]) -> ParamsMaker:
        paramsDto = copy.deepcopy(self.defaultParams)
        for param in extractedParams:
            parts = param.split("=")
            if len(parts) == 2:
                paramsDto.UpdateParameter(parts[0], parts[1])
        return paramsDto
    
    def ParsePattern(self, str: str):
        parts = str.split(":")
        choices = parts.pop(0).split("|")
        settings = self.NormalizeParameters(parts)
        
        weights = []
        for index, choice in enumerate(choices):
            parts = choice.split("%")
            if len(parts) > 1:
                try:
                    num = int(parts[0])
                    weights.append(num)
                    choices[index] = parts[1]
                except:
                    weights.append(1)
            else:
                weights.append(1)
        if len(choices) < 1:
            return ""
        print(choices)
        print(weights)
        chosen = RandomSingleton().choices(choices, weights=weights, k=int(settings.loops))
        if settings.mode == "add":
            occurrences = Counter(chosen)

            result = []
            for word, count in occurrences.items():
                if count > 1:
                    transformed_word = f"({word}:{((count - 1) / 10) + 1})"
                    result.append(transformed_word)
                else:
                    result.append(word)
            chosen = result
        return settings.concatinator.join(chosen)