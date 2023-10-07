import socketio
import time
import config as CONFIG
from Room import Room

# this we will need frequently so saving directly
groupConfigManager = CONFIG.groupConfigManager # object of class GroupConfigManager instantiated in config.py

class MyCustomNamespace(socketio.AsyncNamespace):
    def __init__(self, namespace=None, sio=None):
        super().__init__(namespace=namespace)
        print('construct custom namespace for endpoint --- --->> ', namespace)
        self.namespaceObj = groupConfigManager.getNamespaceObjByEndPoint(
            namespace)
        self.sio = sio  # may be use of BaseManager class will be a better way but we using this of our simple case
        self.ep = namespace  # its confusing if we save value of endpoint as 'namespace', so we name it ep (end-point)
        print('ns base info: ', self.namespaceObj.getBaseInfo())

    async def on_connect(self, sid, environ):
        print(' MCN # 001 ## ', 'on_connect to ns ', {'ns': self.namespaceObj.name, 'sid': sid})
        roomListInfo = self.namespaceObj.roomBaseInfoList
        await self.emit(CONFIG.EVENT['NS_ROOM_LIST'],
                        data=roomListInfo,
                        namespace=self.ep)

    async def on_disconnect(self, sid):
        print(' MCN # 999 ## ', 'disconnecting from: ', {'sid': sid, 'ns ep': self.ep})
        await self.switchSocketToRoom(sid, None)

    async def on_joinRoom(self, sid, switchToRoom):
        print(' MCN # 002 ## ', 'request to join room:  ', {
            'ns': self.namespaceObj.name,
            'room': switchToRoom,
            'sid': sid
        })
        if self.namespaceObj.isValidRoom(switchToRoom):
            await self.switchSocketToRoom(sid, switchToRoom)
            messageList = self.namespaceObj.getRoomByName(switchToRoom).messageList
            print(' MCN # 003 ## ','sending messageList to: ', sid)
            # print(messageList)
            # sending specifically to a client
            await self.sio.emit(CONFIG.EVENT['ROOM_MSG_LIST'],
                                data=messageList,
                                room=sid,
                                namespace=self.ep)
        else:
            print('Server Error: attempt block to join invalid room')

    async def on_message(self, sid, data):
        session_main = await self.sio.get_session(sid)
        roomName = self.getSocketsChatRoomName(sid)

        if roomName != None:
            roomObject = self.namespaceObj.getRoomByName(roomName)
            message = {
                'text': data['text'],
                # 'time': int(time.time()),
                'time': self.myTimeFormatString(),
                'username': session_main['userName'],
                'userId': session_main['userId'],
                'sid': sid,
                'roomName': roomName
            }
            print(' MCN # 004 ## ', message)
            roomObject.addMessage(message)
            # print('to all clients of room send message', message)
            # including the current socket itself, send the message to all the sockets connected to this room
            await self.emit(CONFIG.EVENT['MESSAGE_TO_CLIENT'],
                            data=message,
                            room=roomName,
                            namespace=self.ep)
        else:
            print ('server error: socket is not associated with a room yet in namespace')

    # Though a socket can be connected to several rooms,
    # we restrict it to be connected to just 2 rooms,
    # 1st is default i.e. its own room, & 2nd is one of our chat-rooms from namespace
    async def switchSocketToRoom(self, sid, switchToRoom=None):
        # 1. Find the room where socket is & leave
        switchFromRoom = self.getSocketsChatRoomName(sid)
        if switchFromRoom != None:
            self.leave_room(sid, switchFromRoom, namespace=self.ep)
            await self.updateUserCountOfRoom(sid, switchFromRoom, Room.LEAVE_ROOM_ACTION)
        # 2 Connect to the requested , if it is not None
        if switchToRoom != None:
            self.enter_room(sid, switchToRoom, namespace=self.ep)
            await self.updateUserCountOfRoom(sid, switchToRoom, Room.JOIN_ROOM_ACTION)

    def getSocketsChatRoomName(self, sid):
        # because the socket ALWAYS joins its own room on connection, the 2nd room is the concerned one here
        try:
            print('----------->>>>>>>>>>>>>', self.rooms(sid, namespace=self.ep))
            # return self.rooms(sid, namespace=self.ep)[1]
            duplicate = self.rooms(sid, namespace=self.ep).copy()
            duplicate.remove(sid)
            return duplicate[0]
        except IndexError:
            return None

    async def updateUserCountOfRoom(self, sid, roomName, action):
        roomObject = self.namespaceObj.getRoomByName(roomName)
        if roomObject != None:
            updatedUserCount = roomObject.getUpdatedSidCount(sid, action)
            await self.emit(CONFIG.EVENT['ROOM_USER_COUNT'],
                            data=updatedUserCount,
                            room=roomName,
                            namespace=self.ep)
        else:
            print('Room Name not found: ', roomName)

    def myTimeFormatString(self):
        WEEKDAY_DICT = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        MONTH = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul","Aug", "Sep", "Oct", "Nov", "Dec"]
        struct = time.localtime()
        result=WEEKDAY_DICT[struct.tm_wday]+ ' ' + str(struct.tm_mday)+'. '+str(MONTH[struct.tm_mon])+' '+ str(struct.tm_year)+ ' ' + str(struct.tm_hour) + ':' + str(struct.tm_min)+' '+str(struct.tm_sec)
        return result
