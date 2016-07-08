import re


def message_package_handler(msg, task_pool):
    print '%d messages fetched!'%msg['AddMsgCount']

    for m in msg['AddMsgList']:
        if m['Content'][:22] == '&lt;msg&gt;<br/>&lt;op':
            continue
        print 'From: %s\nMessage: %s\n'%(m['FromUserName'], m['Content'])
        if m['FromUserName'][:2] == '@@':
            task_pool.send_message(to=m['FromUserName'], msg=re.sub('^@[0-9a-z]+:<br/>', '', m['Content']))
            task_pool.query_chatroom_info(m['FromUserName'])
        else:
            task_pool.send_message(to=m['FromUserName'], msg=m['Content'])
