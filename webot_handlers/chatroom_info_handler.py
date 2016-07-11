import pprint as pp
import logging


def chatroom_info_package_handler(context, data):
    logging.info('{0} chatrooms fetched'.format(data['Count']))
    for chatroom in data['ContactList']:
        context.upsert_chatroom(chatroom)
