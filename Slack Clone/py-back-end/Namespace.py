from Room import Room

class Namespace:
    def __init__(self, id, namespaceDict):
        self.roomList = [] # is a list of objects of class Room
        self.roomBaseInfoList = []
        self.id = id
        self.active = namespaceDict['active']
        self.name = namespaceDict['name']
        self.logo = namespaceDict['logo']
        self.endPoint = '/' + namespaceDict['name']
        self._rePopulateRoomList(namespaceDict['rooms'])

    def _rePopulateRoomList(self, roomDictList):
        self.roomList.clear()
        for roomDict in roomDictList:
            roomObj=Room(id=roomDict['id'], name=roomDict['name'], namespace=self)
            self.roomList.append(roomObj)
        self._rebuildRoomBaseInfoList()

    def _rebuildRoomBaseInfoList(self):
        self.roomBaseInfoList.clear()
        for roomObj in self.roomList:
            self.roomBaseInfoList.append(roomObj.getBaseInfo())

    def getBaseInfo(self):
        return {
            "id": self.id,
            "active": self.active,
            "name": self.name,
            "logo": self.logo,
            "endPoint": self.endPoint
        }

    def getRoomByName(self, name):
        return next((x for x in self.roomList if x.name == name), None)

    def isValidRoom(self, roomName):
        if None != next((x for x in self.roomList if x.name == roomName), None):
            return bool(True)
        else:
            return bool(False)


