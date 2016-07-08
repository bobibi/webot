#!/usr/bin/python

import webot_core, response_handler

if __name__ == '__main__':
    res_handler = response_handler.ResponseHandler()
    webot = webot_core.WebotCore()
    webot.start(res_handler)
