# -*- coding: utf-8 -*-

import re
import pprint as pp


MTYPE_VOICE = 34
MTYPE_TEXT = 1


def message_package_handler(context, msg, task_pool):
    print '%d messages fetched!'%msg['AddMsgCount']

    for m in msg['AddMsgList']:
        single_message_handler(context, m, task_pool)


def single_message_handler(context, msg, task_pool):
    # print '>'*40
    # pp.pprint(msg)
    # print '<'*40
    handlers = {
        MTYPE_TEXT: text_message_handler,
        #MTYPE_VOICE: voice_message_handler,
    }
    handlers.get(msg['MsgType'], nop_handler)(context, msg, task_pool)


def nop_handler(context, msg, task_pool):
    print 'Unknow msg type: {0}'.format(msg['MsgType'])
    print 'From: {0} [{1}]'.format(context.get_contact(msg['FromUserName']), msg['FromUserName'])
    print 'Content: {0}'.format(msg['Content'])
    pass


def text_message_handler(context, msg, task_pool):
    if msg['Content'][:22] == '&lt;msg&gt;<br/>&lt;op':
        return

    if msg['FromUserName'][:2] == '@@':
        text_message_handler_chatroom(context, msg, task_pool)
    else:
        text_message_handler_individual(context, msg, task_pool)


def text_message_handler_chatroom(context, msg, task_pool):
    room_id = msg['FromUserName']

    sender_search = re.search('^(@[0-9a-z]+):<br/>', msg['Content'])
    if sender_search is None:
        print 'this is not chatroom message!!'
        return
    sender_id = sender_search.group(1)
    content = re.sub('^@[0-9a-z]+:<br/>', '', msg['Content'])

    chatroom = context.get_chatroom(room_id)
    if chatroom is None:
        task_pool.query_chatroom_info(room_id)
        senderroom = ''
        sender = ''
    else:
        senderroom = chatroom['NickName']
        if sender_id not in chatroom['MemberList']:
            task_pool.query_chatroom_info(room_id)
            sender = ''
        else:
            sender = chatroom['MemberList'][sender_id]['NickName']

    print 'Room: {0} [{1}]'.format(senderroom, room_id)
    print 'Member: {0} [{1}] '.format(sender, sender_id)
    print 'Content: '+content

    said = ''
    if len(sender)>0:
        said = u'{room} 的 {member} 说: '.format(room=senderroom, member=sender)

    task_pool.send_message(to=room_id, msg=said+content)

def text_message_handler_individual(context, msg, task_pool):
    sender_id = msg['FromUserName']
    content = msg['Content']

    contact = context.get_contact(sender_id)
    if contact is not None:
        sender = contact['NickName']
    else:
        task_pool.query_contact()
        sender = ''
    print 'From: {0} [{1}]'.format(sender, sender_id)
    print 'Content: {0}'.format(content)
    task_pool.send_message(to=sender_id, msg=u'{sdr} 说: {msg}'.format(sdr=sender, msg=content))

def voice_message_handler(context, msg, task_pool):
    pass