import pprint as pp


def chatroom_info_package_handler(context, msg):
    print '{0} chatrooms fetched'.format(msg['Count'])
    for chatroom in msg['ContactList']:
        single_chatroom_handler(context, chatroom)

def single_chatroom_handler(context, chatroom):
    roomname = chatroom['UserName']
    if roomname not in context['chatroom']:
        context['chatroom'][roomname] = {}
        context['chatroom'][roomname]['MemberList'] = {}
    context['chatroom'][roomname]['EncryChatRoomId'] = chatroom['EncryChatRoomId']
    context['chatroom'][roomname]['HeadImgUrl'] = chatroom['HeadImgUrl']
    context['chatroom'][roomname]['NickName'] = chatroom['NickName']

    for member in chatroom['MemberList']:
        context['chatroom'][roomname]['MemberList'][member['UserName']] = member

