# -*- coding: utf-8 -*-

import random

call_me_response = [
    u'有什么可以帮助您的呢？',
    u'您有什么需求？请讲吧！',
    u'等一下，我在忙呢！',
    u'Can I help you?',
    u'有事说事！',
]


def parse_and_response(context, obj, task_pool):
    if obj.content.find(context.my_profile['Name']) != -1:
        task_pool.send_message(to=obj.sender_id, msg=random.choice(call_me_response))