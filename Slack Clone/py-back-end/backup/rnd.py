from aiohttp import web
import aiohttp_cors

import asyncio
import socketio

# Creates a new aiohttp Web Application
app = web.Application()

# we can define aiohttp endpoints just as we normally would with no change
# as we do not wish this server to serve any content we hard code expected index.html content
async def index(request):
    return web.Response(text='<html><h1>Hello from Py Backend<h1></html>', content_type='text/html')

# We bind our aiohttp endpoint to our app router
app.router.add_get('/', index)

# we do not wish to use this server as content server, but we wish to serve socket.io.js
app.router.add_static('/socket.io', './static')

# Configure default CORS settings.
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
})

# Configure CORS on all routes.
for route in list(app.router.routes()):
    cors.add(route)

# creates a new Async Socket IO Server
sio = socketio.AsyncServer(async_mode='aiohttp', cors_allowed_origins='*')

# Binds our Socket.IO server to our Web Application instance
sio.attach(app)

@sio.event
async def ping_from_client(sid):
    await sio.emit('pong_from_server', room=sid)

# If we wanted to create a new websocket endpoint,
# use this decorator, passing in the name of the
# event we wish to listen out for
@sio.on('message')
async def print_message(sid, message):
    # When we receive a new event of type
    # 'message' through a socket.io connection
    # we print the socket ID and the message
    print("Socket ID: " , sid)
    print(message)

# THIS is not working in loop - but works independently
# for namespaceObj in groupConfigManager.namespaces:
# print('adding listener for namespace endPoint: '+ namespaceObj.endPoint)
# @sio.event(namespace=namespaceObj.endPoint)
# async def connect(sid, environ):
#     userId = userCount + 1
#     print('connecting to ep '+namespaceObj.endPoint, sid, userId, EVENT['NS_ROOM_LIST'])
#     print(namespaceObj.roomBaseInfoList)
#     await sio.emit(EVENT['NS_ROOM_LIST'], data=namespaceObj.roomBaseInfoList, room=sid, namespace=namespaceObj.endPoint)


# We kick off our server
if __name__ == '__main__':
    web.run_app(app, port=9000)