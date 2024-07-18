from Patterns import FileWildCards, RandomSelector
fileWildCards = FileWildCards.FileWildCards()
randomSelector = RandomSelector.RandomSelector()

def EncodeCharacters(s):
    result = []
    i = 0
    while i < len(s):
        if s[i] != '\\' or i + 1 >= len(s):
            result.append(s[i])
            i += 1
            continue
        next_char = s[i + 1]
        utf8_value = next_char.encode('utf-8').hex()
        result.append(f"&{utf8_value}&")
        i += 2
        
    return ''.join(result)

def DecodeCharacters(self):
    result = []
    i = 0
    while i < len(self):
        if self[i] != '&':
            result.append(self[i])
            i += 1
            continue
        
        end = self.find('&', i + 1)
        if end == -1:
            result.append('&')
            i += 1
            continue
        
        hex_value = self[i+1:end]
        try:
            char = bytes.fromhex(hex_value).decode('utf-8')
            result.append(char)
            i = end + 1
        except ValueError:
            result.append('&')
            i += 1
    return ''.join(result)

OPENER = ["<", "{"]
CLOSER = [">", "}"]
    
def ParseContent(content):
    content = EncodeCharacters(content)
    content = ParseActions(content)
    return content

def ParseActions(str: str):
    result = []
    i = 0
    
    while i < len(str):
        if str[i] in OPENER:
            start = i
            open = str[i]
            close = CLOSER[OPENER.index(open)]
            depth = 1
            i += 1
            while i < len(str) and depth > 0:
                if str[i] == open:
                    depth += 1
                elif str[i] == close:
                    depth -= 1
                i += 1

            if depth == 0:
                inner = str[start+1:i-1]
                parsed = ReplaceAction(inner, open)
                result.append(str[:start])
                result.append(parsed)
                str = str[i:]
                i = 0
        else:
            i += 1
    result.append(str)
    returned = [i for i in result if i is not None]
    return ''.join(returned)
    
def ReplaceAction(inner: str, char: str):
    if char == "<":
        symbol = inner[:1]
        if symbol == "[":
            return fileWildCards.ParsePattern(inner)
        elif symbol == "#":
            return inner
            #get saved param
        elif symbol == "$":
            #append param
            if inner[1:2] == "!":
                return inner
                #set param
            return inner
        
    if char == "{":
        return randomSelector.ParsePattern(inner)