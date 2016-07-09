#!/usr/bin/python

import webot_core, response_handler, webot_context

if __name__ == '__main__':
    res_handler = response_handler.ResponseHandler()
    context = webot_context.WebotContext()
    webot = webot_core.WebotCore()

    webot.start(res_handler, context)
