class Room:
    JOIN_ROOM_ACTION = "join_room"
    LEAVE_ROOM_ACTION = "leave_room"

    def __init__(self, id, name, namespace):
        self.name = name
        self.id = id
        self.namespace = namespace
        self.messageList = []
        self.activeSocketIdSet = set()

    def addMessage(self, message):
        self.messageList.append(message)

    def clearMessages(self):
        self.messageList.clear()

    def getBaseInfo(self):
        return {'id': self.id, 'name': self.name}

    def getUpdatedSidCount(self, sid, action=JOIN_ROOM_ACTION):
        if action == Room.JOIN_ROOM_ACTION:
            self.activeSocketIdSet.add(sid)
        elif action == Room.LEAVE_ROOM_ACTION:
            self.activeSocketIdSet.discard(sid)

        updatedUserCount = len(self.activeSocketIdSet)
        print(
            'getUpdatedSidCount', {
                'roomName': self.name,
                'action': action,
                'sid': sid,
                'count': updatedUserCount
            })
        return updatedUserCount
