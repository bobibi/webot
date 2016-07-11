import webot_handlers.message_handler as msg_handler
import webot_handlers.contact_handler as contact_handler
import webot_handlers.chatroom_info_handler as cr_info_handler
import webot_handlers.wechat_init_handler as init_handler
from webot_task_pool import WebotTaskPool
import sys, traceback
import pprint as pp
import logging, webot_logging


class ResponseHandler(object):
    def __init__(self):
        logging.info('Response handler init ...')

    def wechat_init(self, context, msg):
        reload(init_handler)
        try:
            init_handler.wechat_init(context, msg)
        except Exception as e:
            traceback.print_exc(file=webot_logging.log_file)
            logging.warning('Wechat init handler failed: %s', e)

    def wechat_contact(self, context, msg):
        reload(contact_handler)
        try:
            contact_handler.contact_package_handler(context, msg)
        except Exception as e:
            traceback.print_exc(file=webot_logging.log_file)
            logging.warning('Wechat contact handler failed: %s', e)

    def wechat_sync(self, context, msg):
        #pp.pprint(msg)
        pass

    def wechat_message(self, context, msg):
        reload(msg_handler)
        task_pool = WebotTaskPool()
        try:
            msg_handler.message_package_handler(context, msg, task_pool)
        except Exception as e:
            traceback.print_exc(file=webot_logging.log_file)
            logging.warning('Wechat message handler failed: %s', e)

        return task_pool

    def wechat_chatroom_info(self, context, msg):
        reload(cr_info_handler)
        try:
            cr_info_handler.chatroom_info_package_handler(context, msg)
        except Exception as e:
            traceback.print_exc(file=webot_logging.log_file)
            logging.warning('Wechat chatroom info handler failed: %s', e)