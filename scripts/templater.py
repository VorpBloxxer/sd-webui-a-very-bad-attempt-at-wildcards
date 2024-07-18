import os, yaml

def GetWcDirectory():
    current = os.path.dirname(os.path.realpath(__file__))
    extension = os.path.abspath(os.path.join(current, os.pardir))
    return os.path.join(extension, 'Wildcards')

def GetModplatesDirectory():
    current = os.path.dirname(os.path.realpath(__file__))
    extension = os.path.abspath(os.path.join(current, os.pardir))
    return os.path.join(extension, 'Modplates')

def GetTemplatesDirectory():
    current = os.path.dirname(os.path.realpath(__file__))
    extension = os.path.abspath(os.path.join(current, os.pardir))
    return os.path.join(extension, 'Templates')
        
def PreloadFolders(_, app):
    folders = ['Wildcards', 'Modplates', 'Templates']
    current = os.path.dirname(os.path.realpath(__file__))
    extension = os.path.abspath(os.path.join(current, os.pardir))
    for folder in folders:
        directory = os.path.join(extension, folder)
        if not os.path.exists(directory):
            os.makedirs(directory)  

def ModplatesFromModel(model_name: str) -> dict:
    templates_directory = GetModplatesDirectory()
    file_path = os.path.join(templates_directory, f"{model_name}.yaml")
    
    if not os.path.isfile(file_path):
            templates = {}
            
            with open(file_path, 'w') as file:
                yaml.safe_dump(templates, file)
    else:
        with open(file_path, 'r') as file:
            templates = yaml.safe_load(file)
            if templates is None:
                templates = {}
                
    return templates

class SingletonClass(object):
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SingletonClass, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.currentKeywords = ""
            self.currentModPlate = ""
            self.initialized = True

    def ModplatesNames(model_name: str) -> list:
        templates = ModplatesFromModel(model_name)
        template_names = list(templates.keys())
        return template_names

    def loadModplates(model_name: str, template_name: str):
        templates = ModplatesFromModel(model_name)
        
        if templates[template_name]:
            return templates[template_name]
        
        return {}

    def AddOrUpdModplate(model_name: str, template_name: str, contentDict=None):
        folder_path = GetModplatesDirectory()
        templates = ModplatesFromModel(model_name)
        print(f"template_name : {template_name}")
        if contentDict == None:
            contentDict = {}
        
        if template_name == "Random":
            return "Template Cannot be named that way"

        if template_name in templates:
            templates.update({template_name: contentDict})
        else:
            templates[template_name] = contentDict
            
        file_path = os.path.join(folder_path, f"{model_name}.yaml")
        with open(file_path, 'w') as file:
            yaml.safe_dump(templates, file)
        
        return "Template saved!"
    
    def SetCurrentModplate(self, modplate):
        print("Current ModPlate: \n" + modplate)
        self.currentModPlate = modplate
        
    def SetCurrentKeywordPlate(self, keywordplate):
        print("Current KeywordPlate: \n" + keywordplate)
        self.currentKeywords = keywordplate