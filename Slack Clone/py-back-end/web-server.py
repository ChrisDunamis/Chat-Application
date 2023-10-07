from aiohttp import web

import socket_impl as socket_impl
import config as CONFIG

# Creates a new aiohttp Web Application
web_application = web.Application()

# we can define aiohttp endpoints just as we normally would with no change
# as we do not wish this server to serve any content we hard code expected index.html content
async def index(request):
    return web.Response(text='<html><h1>Hello from Py Backend<h1></html>', content_type='text/html')

# We bind our aiohttp endpoint to our app router
web_application.router.add_get('/', index)

socket_impl.init(web_application)

# We kick off our server
if __name__ == '__main__':
    print(('##### Python Backend listening on PORT:' + str(CONFIG.PORT)))
    web.run_app(web_application, port=CONFIG.PORT)
