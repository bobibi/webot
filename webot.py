#!/usr/bin/python
import webot_logging, logging
import webot_core, response_handler, webot_context


if __name__ == '__main__':
    webot_logging.init()
    logging.info('Webot starting ...')
    res_handler = response_handler.ResponseHandler()
    context = webot_context.WebotContext()
    webot = webot_core.WebotCore()

    webot.start(res_handler, context)
