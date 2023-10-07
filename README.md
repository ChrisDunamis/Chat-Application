# Chat-Application

## Terminologies
1. Web server (hosts the UI/Content)
2. Application server (backend - performs the logic)
3. Client/End-user

## Features
- Multi-client chat application
- Configure workspace & rooms via JSON
- Bootstrap/CSS-grid UI
- Real-time user count in a given channel (room)
- Chat history
- Console debug statements to explain the flow
- A client can be active in 1 room of a channel

## Restrictions:
- No login/logout
- Cannot add workspace or channel from the client side
- Will not persist chat history on server side or client side (after server shutdown)
- ___Note:___ The contents of the user session are destroyed when the client disconnects. In particular, user session contents are not preserved when a client reconnects after an unexpected disconnection from the server.

## Installation Steps:

### ___Front-End___
- execute `(chmod +x front-end/server.sh)`

To start the front-end server:
- execute `cd front-end`
- execute `./server.sh`

### ___Back-End___
Execute the following from the py-back-end folder:

- pip3 install wheel
- pip3 install python-socketio
- pip3 install asyncio
- pip3 install aiohttp
- pip3 install aiohttp_cors

To start the back-end server:
- execute `cd py-back-end`
- execute `python3 web-server.py`
