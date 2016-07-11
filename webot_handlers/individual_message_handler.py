# -*- coding: utf-8 -*-
from message_interpreter import text_command
import logging


def text_message(context, obj, task_pool):
    contact = context.get_contact(obj.sender_id)
    if contact is not None:
        sender_name = contact['NickName']
    else:
        task_pool.query_contact()
        sender_name = ''
    logging.info(u'From: {0} [{1}]'.format(sender_name, obj.sender_id))
    logging.info(u'Content: {0}'.format(obj.content))

    text_command.parse_and_response(context, obj, task_pool)
    #task_pool.send_message(to=obj.sender_id, msg=u'{sdr} 说: {msg}'.format(sdr=sender_name, msg=obj.content))