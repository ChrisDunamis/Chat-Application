from GroupConfigManager import GroupConfigManager

PORT = 9000

# for better administration, dictionary/map of all events used in app.
EVENT = {
    'NS_INFO_LIST': 'namespaceInfoList',
    'NS_ROOM_LIST': 'namespaceRoomList',
    'ROOM_MSG_LIST': 'roomMessageList',
    'ROOM_USER_COUNT': 'updateRoomUserCount',
    'MESSAGE_TO_CLIENT': 'message',
    'MESSAGE_TO_SERVER': 'message',
    'REQ_CONNECTION': 'connection',
    'REQ_JOIN_ROOM': 'joinRoom',
}

# load namespace room configuration file
GROUP_CONFIG_PATH = './group_config.json'
groupConfigManager = GroupConfigManager(GROUP_CONFIG_PATH)

print('###### ######')
