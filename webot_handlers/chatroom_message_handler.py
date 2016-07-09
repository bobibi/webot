# -*- coding: utf-8 -*-
from message_interpreter import text_command


def text_message(context, obj, task_pool):
    chatroom = context.get_chatroom(obj.sender_id)
    if chatroom is None:
        task_pool.query_chatroom_info(obj.sender_id)
        room_name = ''
        member_name = ''
    else:
        room_name = chatroom['NickName']
        if obj.member_id not in chatroom['MemberList']:
            task_pool.query_chatroom_info(obj.sender_id)
            member_name = ''
        else:
            member_name = chatroom['MemberList'][obj.member_id]['NickName']

    print u'Room: {0} [{1}]'.format(room_name, obj.sender_id)
    print u'Member: {0} [{1}] '.format(member_name, obj.member_id)
    print u'Content: {0}'.format(obj.content)

    said = ''
    if len(member_name)>0:
        said = u'{room} 的 {member} 说: '.format(room=room_name, member=member_name)

    text_command.parse_and_response(context, obj, task_pool)
    #task_pool.send_message(to=obj.sender_id, msg=said+obj.content)


def money_message(context, obj, task_pool):
    chatroom = context.get_chatroom(obj.sender_id)
    if chatroom is None:
        task_pool.query_chatroom_info(obj.sender_id)
        room_name = '某个群'
    else:
        room_name = chatroom['NickName']

    print u'Room: {0} [{1}]'.format(room_name, obj.sender_id)
    print u'Content: {0}'.format(obj.content)
    notify_user = [u'小娃儿曾万万', u'曾千千小娃儿']
    for nu in notify_user:
        cid = context.get_contact_id(nu)
        if cid is None:
            print u'cannot find contact id for {0}'.format(nu)
            continue
        task_pool.send_message(to=cid, msg=u'{0} 里有人发红包啦! 快去抢啊!'.format(room_name))