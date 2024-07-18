import os, yaml

def file_tree_dict(path):
        result = {}

        if os.path.isfile(path):
            with open(path, 'r') as file:
                try:
                    result[os.path.basename(path)] = file.read()
                except:
                    print(f"file {file} isn't a valid txt or yaml")
        elif os.path.isdir(path):
            result[os.path.basename(path)] = {}
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                result[os.path.basename(path)].update(file_tree_dict(item_path))

        return result

def decode_dictionary(dictionary, path='', fileDict={}):
    fileDict = fileDict

    for key, value in dictionary.items():
        new_path = os.path.join(path, key)
        new_path = new_path.replace("\\", "/")
        if isinstance(value, dict):
            decode_dictionary(value, new_path, fileDict)
        else:
            if key.endswith('.txt'):
                fileDict[new_path] = {"value": value, "type": 'txt'}
            elif key.endswith('.yaml'):
                cleaned_yaml = '\n'.join(line for line in value.split('\n') if not line.strip().startswith('#'))
                yaml_data = yaml.safe_load(cleaned_yaml)
                fileDict[new_path] = {"value": yaml_data, "type": 'yaml'}

    return fileDict

def loadFiles():
    current_directory = os.path.dirname(os.path.realpath(__file__))
    parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
    wildcards_directory = os.path.join(parent_directory, 'wildcards')

    tree_dict = file_tree_dict(wildcards_directory)

    file_list = decode_dictionary(tree_dict)

    return file_list

def display_tree(path, indent=''):
    if os.path.isfile(path):
        print(indent + os.path.basename(path))
    elif os.path.isdir(path):
        print(indent + os.path.basename(path) + '/')
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            display_tree(item_path, indent + '  ')

class FileLoader(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FileLoader, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.files = loadFiles()
            self.initialized = True
    
    def reload(self):
        self.files = loadFiles()

import random as Random
class RandomSingleton(Random.Random):
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RandomSingleton, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.initialized = True