/**
 * For a given EndPoint string which essentially starts with '/', this function does the following
 * 1) If the namespaceSocket is already associated, disconnect it
 * 2) Connects to the requested endpoint
 * 3) Once server get to know some one got connected to namespace it emits list of rooms & we update our DOM
 *    While updating DOM, we also embed event listener that helps to switch room
 * 4) Join the 1st room from list, by default - when entering namespace
 * @param {String} endPoint
 */
function joinNamespace(endPoint){
    console.debug(`Requested to join the namespace with end point: ${endPoint}`);
    // from previous namespace connection - cleaning is required
    if(namespaceSocket){
        // check to see if namespaceSocket is actually a socket
        namespaceSocket.close();
    }

    // connect to the desired namespace
    namespaceSocket = io(`${serverHostUrl}${endPoint}`);

    // if connecting to oa valid endPoint we anticipate list-of-rooms to be shared by server
    namespaceSocket.on(EVENT.NS_ROOM_LIST,(nsRooms)=>{
        console.debug('List of Rooms of the namespace: ',nsRooms);

        // update the room-list section
        let roomList = document.querySelector('.room-list');
        roomList.innerHTML = "";
        nsRooms.forEach(({name})=>{
            roomList.innerHTML += `<li class="room">${name}</li>`
        })

        // add click listener to each room
        let roomNodes = document.getElementsByClassName('room');
        Array.from(roomNodes).forEach((element)=>{
            element.addEventListener('click',(e)=>{
                joinRoom(e.target.innerText)
            })
        })

        // by default join the 1st room
        joinRoom(nsRooms[0].name);
    })

    // When some one send message to the room of namespace, we update message list
    namespaceSocket.on(EVENT.MESSAGE_TO_CLIENT,(message)=>{
        console.debug('messsage received: ', message)
        const messagesUl = document.querySelector('#messageList');
        messagesUl.innerHTML += buildMessageHTML(message);

        // as we wish to see the most recent message on the screen
        scrollToMostRecentMessage();
    })
}
