
import json
from Namespace import Namespace

class GroupConfigManager:
    def __init__(self, configFilePath):
        self.namespaces = [] # is a list of objects of class Namespace
        self.namespaceBaseInfoList = []
        self._rePopulateNamespaceObjectList(configFilePath)

    def getNamespaceBaseInfoList(self):
        return self.namespaceBaseInfoList

    def getNamespaceObjByName(self, name):
        return next((x for x in self.namespaces if x.name == name), None)

    def getNamespaceObjByEndPoint(self, endPoint):
        return next((x for x in self.namespaces if x.endPoint == endPoint), None)

    def _rebuildNamespaceBaseInfoList(self):
        self.namespaceBaseInfoList.clear()
        for namespace in self.namespaces:
            self.namespaceBaseInfoList.append(namespace.getBaseInfo())

    def _rePopulateNamespaceObjectList(self, configFilePath):
        self.namespaces.clear()
        with open(configFilePath) as f:
            GROUP_CONFIG = json.load(f)
            for key, value in GROUP_CONFIG.items():
                # print(key, value)
                namespaceObject = Namespace(id=key, namespaceDict=value)
                self.namespaces.append(namespaceObject)
            self._rebuildNamespaceBaseInfoList()

# GROUP_CONFIG_PATH = './group_config.json'
# groupConfigManager = GroupConfigManager(GROUP_CONFIG_PATH)