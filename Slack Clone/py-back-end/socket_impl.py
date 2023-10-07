import socketio

import config as CONFIG

from MyCustomNamespace import MyCustomNamespace

# Just to read the queryParameters
from urllib.parse import parse_qs

groupConfigManager = CONFIG.groupConfigManager

# creates a new Async Socket IO Server
sio = socketio.AsyncServer(async_mode='aiohttp', cors_allowed_origins='*')

def init(web_application):
    # Binds our Socket.IO server to our Web Application instance
    sio.attach(web_application)

    sio.userCount = 0  # helps UI to pick avatar & name colors

    for namespaceObj in groupConfigManager.namespaces:
        customNameSpaceObject = MyCustomNamespace(namespaceObj.endPoint, sio)
        sio.register_namespace(customNameSpaceObject)

@sio.event(namespace='/')
async def connect(sid, environ):
    await saveUserNameIfExists(sid, environ)
    print(' 001 ## connecting to default namespace', sid, await sio.get_session(sid))
    await sio.emit(CONFIG.EVENT['NS_INFO_LIST'],
                   groupConfigManager.namespaceBaseInfoList,
                   room=sid)

@sio.event(namespace='/')
async def disconnect(sid):
    print(' 999 ## disconnecting from default namespace ', sid, await sio.get_session(sid))

@sio.event(namespace='/')
async def message(sid, data):
    session = await sio.get_session(sid)
    print('message from ', session['username'])
    print('By the way why is someone sending message to default namespace !!')

async def saveUserNameIfExists(sid, environ):
    # print('------ ', environ['QUERY_STRING'])
    queryDict = parse_qs(environ['QUERY_STRING'])
    if "username" in queryDict:
        userNameArray = queryDict["username"]
        if userNameArray != None and len(userNameArray) > 0:
            sio.userCount += 1
            userName = userNameArray[0]
            sessionData = {
                'userName': userName,
                'userId': sio.userCount,
                'sid': sid
            }
            # print('=== ====', sessionData)
            await sio.save_session(sid, sessionData)
