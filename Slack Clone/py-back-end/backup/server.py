# pip3 install wheel
# pip3 install python-socketio
# pip3 install web
# pip3 install aiohttp
# pip3 install aiohttp_cors

from aiohttp import web

import asyncio
import socketio

import config as CONFIG

from MyCustomNamespace import MyCustomNamespace

# Just to read the queryParameters
from urllib.parse import parse_qs

# this we will need frequently so saving directly
EVENT = CONFIG.EVENT

groupConfigManager = CONFIG.groupConfigManager

# Creates a new aiohttp Web Application
web_application = web.Application()

# creates a new Async Socket IO Server
sio = socketio.AsyncServer(async_mode='aiohttp', cors_allowed_origins='*')

# Binds our Socket.IO server to our Web Application instance
sio.attach(web_application)

sio.userCount = 0  # helps UI to pick avatar & name colors

for namespaceObj in groupConfigManager.namespaces:
    customNameSpace = MyCustomNamespace(namespaceObj.endPoint, sio)
    sio.register_namespace(customNameSpace)

@sio.event(namespace='/')
async def connect(sid, environ):
    print('connecting to default namespace', sid)
    await saveUserNameIfExists(sid, environ)
    await sio.emit(EVENT['NS_INFO_LIST'],
                   groupConfigManager.namespaceBaseInfoList,
                   room=sid)

@sio.event(namespace='/')
async def disconnect(sid):
    print('disconnect ', sid)

@sio.event(namespace='/')
async def message(sid, data):
    session = await sio.get_session(sid)
    print('message from ', session['username'])
    print('By the way why is someone sending message to default namespace !!')

async def saveUserNameIfExists(sid, environ):
    queryDict = parse_qs(environ['QUERY_STRING'])
    if "username" in queryDict:
        userNameArray = queryDict["username"]
        if userNameArray != None and len(userNameArray) > 0:
            sio.userCount += 1
            userName = userNameArray[0]
            sessionData = {
                'sid': sid,
                'userId': sio.userCount,
                'userName': userName
            }
            print('=== ====', sessionData)
            await sio.save_session(sid, sessionData)

# @sio.event(namespace='/')
# async def disconnect(sid):
#     print('disconnect ', sid)

# @sio.on(EVENT['REQ_JOIN_ROOM'], namespace='/fun')
# async def print_message(sid, message):
#     print("Socket ID: " , sid)
#     print(message)

# we can define aiohttp endpoints just as we normally would with no change
# as we do not wish this server to serve any content we hard code expected index.html content
async def index(request):
    return web.Response(text='<html><h1>Hello from Py Backend<h1></html>', content_type='text/html')

# We bind our aiohttp endpoint to our app router
web_application.router.add_get('/', index)

# We kick off our server
if __name__ == '__main__':
    print(('##### Python Backend listening on PORT:' + str(CONFIG.PORT)))
    web.run_app(web_application, port=CONFIG.PORT)
