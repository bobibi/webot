import webot_handlers.message_handler as msg_handler
from webot_task_pool import WebotTaskPool

class ResponseHandler(object):
    def __init__(self):
        print 'response handler init'

    def wechat_init(self, msg):
        print msg

    def wechat_contact(self, msg):
        print msg

    def wechat_sync(self, msg):
        print msg

    def wechat_message(self, msg):
        reload(msg_handler)
        task_pool = WebotTaskPool()
        try:
            msg_handler.message_package_handler(msg, task_pool)
        except:
            print 'message handler cannot run!!'

        return task_pool

    def wechat_chatroom_info(self, msg):
        print msg