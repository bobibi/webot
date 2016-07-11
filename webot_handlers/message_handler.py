# -*- coding: utf-8 -*-

import re, logging
import pprint as pp
import individual_message_handler as imh
import chatroom_message_handler as cmh

SDR_TYPE_CHATROOM = 0
SDR_TYPE_INDIVIDUAL = 1

MTYPE_VOICE = 34
MTYPE_TEXT = 1
MTYPE_MONEY = 10000
MTYPE_SYNC = 51
MTYPE_PHOTO = 3
MTYPE_EMOICON = 47


class WechatMessage(object):
    def __init__(self, data):
        self.sender_id = data['FromUserName']
        self.content = data['Content']
        self.member_id = None
        self.message_type = data['MsgType']

        if self.sender_id[:2] == '@@':
            self.sender_type = SDR_TYPE_CHATROOM
            sender_search = re.search('^(@[0-9a-z]+):<br/>', self.content)
            if sender_search is not None:
                self.member_id = sender_search.group(1)
                self.content = re.sub('^@[0-9a-z]+:<br/>', '', self.content)
        else:
            self.sender_type = SDR_TYPE_INDIVIDUAL


def message_package_handler(context, msg, task_pool):
    logging.info(u'%d messages fetched!'%msg['AddMsgCount'])

    for m in msg['AddMsgList']:
        msg_obj = WechatMessage(m)
        single_message_handler(context, msg_obj, task_pool)


def single_message_handler(context, obj, task_pool):
    handlers = {
        SDR_TYPE_INDIVIDUAL: {
            MTYPE_TEXT: imh.text_message,
        },
        SDR_TYPE_CHATROOM: {
            MTYPE_TEXT: cmh.text_message,
            MTYPE_MONEY: cmh.money_message,
        }
    }
    sender_handler = handlers.get(obj.sender_type, {})
    msg_handler = sender_handler.get(obj.message_type, nop_handler)
    msg_handler(context, obj, task_pool)


def nop_handler(context, obj, task_pool):
    contact = context.get_contact(obj.sender_id)
    logging.info(u'Unknow msg type: {0}'.format(obj.message_type))
    logging.info(u'From: {0} [{1}]'.format('' if contact is None else contact['NickName'], obj.sender_id))
    logging.info(u'Content: {0}'.format(obj.content))
