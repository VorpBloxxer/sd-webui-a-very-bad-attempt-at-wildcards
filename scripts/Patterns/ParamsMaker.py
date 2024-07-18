from abc import abstractmethod
def ExtractBrackets(input_string):
    result = []
    count = 0
    temp = ''

    for char in input_string:
        if char == '[':
            count += 1
            if count == 1:
                temp = ''
            elif count > 1:
                temp += char
        elif char == ']':
            count -= 1
            if count == 0:
                if temp != '':
                    result.append(temp)
                temp = ''
            elif count > 0:
                temp += char
        elif count > 0:
            temp += char

    return result

class ParamsMaker:
    def __init__(self, **kwargs):
        self.aliases = {}
        for paramName, paramDetails in kwargs.items():
            if isinstance(paramDetails, tuple):
                defaultValue, *aliases = paramDetails
                for alias in aliases:
                    self.aliases[alias] = paramName
            else:
                defaultValue = paramDetails
            setattr(self, paramName, defaultValue)

    def UpdateParameter(self, paramName, value):
        if paramName in self.aliases:
            paramName = self.aliases[paramName]
        
        if hasattr(self, paramName):
            currentValue = getattr(self, paramName)
            valueType = type(currentValue)
            try:
                convertedValue = valueType(value)
                setattr(self, paramName, convertedValue)
            except (ValueError, TypeError) as e:
                raise TypeError(f"Cannot convert value '{value}' to type {valueType.__name__} for attribute {paramName}") from e
        else:
            raise AttributeError(f"{paramName} is not a valid attribute of {self.__class__.__name__}")
        
class IPattern():
    @abstractmethod
    def NormalizeParameters(self, extractedParams: dict[str, str]):
        pass
    
    @abstractmethod
    def ParsePattern(self):
        pass