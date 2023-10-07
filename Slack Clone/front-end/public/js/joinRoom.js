/**
 * For a given room-name string, this function does the following
 * 1) Signals server to let socket be connected to a room
 * 2) Server disconnects the socket from previous room and connects to the requested one & then it emits the
 *    List of messages of the new room
 * 3) Update the messages in the messageboard
 * 4) Listen to event that shares current user count and update on top of message board
 * 5) Update room name at the top of message board
 * @param {String} roomName
 */
function joinRoom(roomName){
    // Inform server this socket wish to be now connected to a new room!
    namespaceSocket.emit(EVENT.REQ_JOIN_ROOM, roomName);

    // When we join a room, server sends us list of messages of that room
    namespaceSocket.on(EVENT.ROOM_MSG_LIST,(history)=>{
        const messagesUl = document.querySelector('#messageList');
        messagesUl.innerHTML = "";
        history.forEach((msg)=>{
            const newMsg = buildMessageHTML(msg)
            messagesUl.innerHTML += newMsg;
        })

        // as we wish to see the most recent message on the screen
        scrollToMostRecentMessage()
    })

    // whenever some one join/leave room server informs us the new activeUserCount
    namespaceSocket.on(EVENT.ROOM_USER_COUNT,(activeUserCount)=>{
        document.querySelector('.curr-room-num-users').innerHTML = `${activeUserCount}`
    })

    // Lets update the name of room in room header
    document.querySelector('.curr-room-name').innerText = `${roomName}`

    // highlight selected room
    highlightedSelectedRoom(roomName);
};

function highlightedSelectedRoom(roomName) {
    let roomNodes = Array.from(document.getElementsByClassName('room'));
    roomNodes.forEach((ele) => ele.classList.remove('active'));
    const [selectedRoom] = roomNodes.filter((ele) => (ele.innerText === roomName));
    selectedRoom.classList.add('active');
}