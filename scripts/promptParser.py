from usefulClasses import *
from stringManipulation import *

fileLoader = FileLoader()
randomSingleton = RandomSingleton()

class PromptParser(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PromptParser, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.currentPromptObject = None
            self.PromptAttributes = []
            self.lastParse = ""
            self.currentParse = ""
            self.initialized = True
    
    def ParseLoop(self):
        finished = False
        while not finished:
            self.currentParse = ParseContent(self.lastParse)
            if self.currentParse != self.lastParse:
                self.lastParse = self.currentParse
                continue
            finished = True
        return DecodeCharacters(self.currentParse)
    
    # def ReloadFiles(self):
    #     FileLoader.reload()
            
parser = PromptParser()
print("Starting test")
#parser.lastParse = "{red|blue|green} <[__testing__][ConstructTest]:n=3:concat= and > <[__colors/__]:n=2> \<[NoParse]\>"

parser.lastParse = "{100%red|blue|green:n=3} <[PaletteMakerTest]:params=[red][blue]>"
print(parser.ParseLoop())