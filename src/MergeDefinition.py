import json
import sys

# todo jsonデータの型をいい感じに指定したい
class MergeDefinition:
    def __init__(self, path:str) -> None:
        self.path = path
        self.load()

    def load(self):
        file = open(self.path, 'r')
        self.json = json.load(file)
        sys.stdout.write("'{0}' load successed.\ndefinition version is {1}.\n".format(self.path, self.getVersion()))

    def getVersion(self) -> int:
        return self.json['version']

    def getDefinitions(self) -> list[list]:
        return self.json['definitions']
