

class WebotTaskPool(object):
    def __init__(self):
        self.out_messages = []
        self.chatrooms_need_info = []
        self.refresh_contact = False

    def send_message(self, to, msg):
        self.out_messages.append({'to': to, 'msg': msg})

    def query_chatroom_info(self, room):
        self.chatrooms_need_info.append(room)

    def query_contact(self):
        self.refresh_contact = True