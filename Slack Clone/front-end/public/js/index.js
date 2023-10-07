// for better administration, dictionary/map of all events used in app.
const EVENT = {
    'NS_INFO_LIST'   : 'namespaceInfoList', // list of namespace-info coming from server
    'NS_ROOM_LIST'   : 'namespaceRoomList', // list of room-info coming from server - of a namespace
    'ROOM_MSG_LIST'  : 'roomMessageList',   // list of messages-info coming from server - of a room oof namespace
    'ROOM_USER_COUNT': 'updateRoomUserCount', // coming from server count of users of a room, whenever updated

    'MESSAGE_TO_CLIENT' : 'message',
    'MESSAGE_TO_SERVER' : 'message',

    'REQ_CONNECTION'    : 'connection', // client is requesting server to let him connect to chatting system
    'REQ_JOIN_ROOM'     : 'joinRoom', // client is requesting server to join a room in a given namespace
};

// client connects to froont-endserver and loads chat application UI code+resources
// client send request for connection to chat-application-server
// when response is received from server - containign handshake info, and by default clients get connected to default namespace '/'
// once the connection is established server sends event to that specific client about the list of namespaces
// client update the HTML DOM - with the namespace list
// client joins one of the namespace - doing so it tells server
// server sends information of all the rooms of that namespace - and client update its DDM whenever server sends this info (i.e. whenever name space is switched)
// client automatically joins the top-room from the list ( Using UI user can select any room to join) - request to join room is sent to server - server let the client join that room and sends back the list of messages of that room
// client update its message board with the messages
// whenever some one enter or leave a room, server sends the new active-user count info ONLY to all the active users of the room ( not al users currently connected to server)
// A user can send message from within a room, server distributes that message only to the current active users of room


const COLORS = [
    '#f78b00', '#287b00', '#3824aa', '#a700ff', '#e21400', '#91580f'
];

const username = prompt("What is your username?");

const serverHostUrl = 'http://localhost:9000';

// this connects to default namespace '/'
const socket = io(serverHostUrl, {
    query: {
        username
    }
});

let namespaceSocket = "";

// listen for namespace base info list, which is a list of all the namespaces.
socket.on(EVENT.NS_INFO_LIST,(namespaceBaseInfoList)=>{
    console.debug(`Base Info of Namespace: \n ${JSON.stringify(namespaceBaseInfoList)}`);

    // populate namespace list
    const namespacesDiv = document.querySelector('.namespaces-list');
    namespacesDiv.innerHTML = "";
    namespaceBaseInfoList.forEach((namespace)=>{
        const {endPoint, logo} = namespace;
        namespacesDiv.innerHTML += `<div class="namespace" ns=${endPoint} ><img src="${logo}" /></div>`
    })

    // Add a clicklistener for each NS
    Array.from(namespacesDiv.getElementsByClassName('namespace')).forEach((element)=>{
        console.debug('namespaces-list element', element);
        element.addEventListener('click',(e)=>{
            const nsEndPoint = element.getAttribute('ns');
            joinNamespace(nsEndPoint);
        })
    })

    // join the topmost namespace
    joinNamespace(namespaceBaseInfoList[0].endPoint);
})

//
document.querySelector('.message-form').addEventListener('submit',sendMessageToServer)

function sendMessageToServer(event){
    // though we know here that to which room we have to send message, but we send to namespace only, as on server we manage that a namespaceSocket is active only in 1 room (except default), server also knows which room and hence server send notification only to the currently active sockets of room
    event.preventDefault();
    const textMessage = document.querySelector('#user-message').value;

    namespaceSocket.emit(EVENT.MESSAGE_TO_SERVER,{text: textMessage});

    document.querySelector('#user-message').value = ""; // clear the message which is transmitted
}

function buildMessageHTML(message){
    const {userId, username, text, time} = message;
    // const convertedDate = new Date(time).toLocaleString();
    const convertedDate = time;
    const userCode = userId%6;
    const avatar = `http://localhost:8000/resources/avatars/${userCode}.svg`
    const messageHTML = `
    <li>
        <div class="user-image">
            <img src="${avatar}" />
        </div>
        <div class="user-message">
            <div class="user-name-time" style="color:${COLORS[userCode]}"> [ ${username} <span>${convertedDate}</span> ]</div>
            <div class="message-text">${text}</div>
        </div>
    </li>
    `
    return messageHTML;
}

function scrollToMostRecentMessage() {
    const messagesUl = document.querySelector('#messageList');
    messagesUl.scrollTo(0,messagesUl.scrollHeight);
    // later CSS can be updated such that messageboard fits too screen and only the messageList remains scrollable
    const messageBoard = document.querySelector('.message-board')
    messageBoard.scrollTo(0,messageBoard.scrollHeight);
}

// search box feature
let searchBox = document.querySelector('#search-box');
searchBox.addEventListener('input',(e)=>{
    console.log(e.target.value)
    let messages = Array.from(document.getElementsByClassName('message-text'));
    console.debug('search filter messages ', messages);
    messages.forEach((msg)=>{
        if(msg.innerText.toLowerCase().indexOf(e.target.value.toLowerCase()) === -1){
            // the msg does not contain the user search term!
            msg.parentElement.parentElement.style.display = "none";
        }else{
            msg.parentElement.parentElement.style.display = "flex"
        }
    })
})
