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
        MTYPE_VOICE: voice_message_handler,
    }
    handlers.get(msg['MsgType'], nop_handler)(context, msg, task_pool)


def nop_handler(context, msg, task_pool):
    pass


def text_message_handler(context, msg, task_pool):
    if msg['Content'][:22] == '&lt;msg&gt;<br/>&lt;op':
        return

    if msg['FromUserName'][:2] == '@@':
        text_message_handler_chatroom(context, msg, task_pool)
    else:
        text_message_handler_individual(context, msg, task_pool)


def text_message_handler_chatroom(context, msg, task_pool):
    senderroom_id = msg['FromUserName']
    content = msg['Content']

    sender_search = re.search('^(@[0-9a-z]+):<br/>', content)
    if sender_search is None:
        print 'this is not chatroom message!!'
        return
    sender_id = sender_search.group(1)
    content = re.sub('^@[0-9a-z]+:<br/>', '', content)

    if senderroom_id not in context['chatroom']:
        task_pool.query_chatroom_info(senderroom_id)
        senderroom = ''
        sender = ''
    else:
        senderroom = context['chatroom'][senderroom_id]['NickName']
        if sender_id not in context['chatroom'][senderroom_id]['MemberList']:
            task_pool.query_chatroom_info(senderroom_id)
            sender = ''
        else:
            sender = context['chatroom'][senderroom_id]['MemberList'][sender_id]['NickName']

    print 'Room: '+senderroom
    print 'Member: '+sender
    print 'Content: '+content

    said = ''
    if len(sender)>0:
        said = u'{room} 的 {member} 说: '.format(room=senderroom, member=sender)

    task_pool.send_message(to=senderroom_id, msg=said+content)

def text_message_handler_individual(context, msg, task_pool):
    sender_id = msg['FromUserName']
    content = msg['Content']

    if sender_id in context['contact']:
        sender = context['contact'][sender_id]['NickName']
        print 'From: %s\nMessage: %s\n'%(context['contact'][sender_id]['NickName'], content)
    else:
        task_pool.query_contact()
        sender = 'UNKNOWN'
        print 'From: %s\nMessage: %s\n'%(sender_id, content)

    task_pool.send_message(to=sender_id, msg=u'{sdr}说: {msg}'.format(sdr=sender, msg=content))

def voice_message_handler(context, msg, task_pool):
    pass