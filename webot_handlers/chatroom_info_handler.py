import pprint as pp


def chatroom_info_package_handler(context, data):
    print '{0} chatrooms fetched'.format(data['Count'])
    for chatroom in data['ContactList']:
        context.upsert_chatroom(chatroom)
