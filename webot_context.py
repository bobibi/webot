import time
import pprint as pp


class WebotContext(object):
    def __init__(self):
        self.contact = {}
        self.contact_timestamp = 0
        self.chatroom = {}
        self.chatroom_timestamp = {}

    def upsert_contact(self, data):
        contact_id = data['UserName']
        contact_name = data['NickName']
        self.contact[contact_id] = data
        self.contact_timestamp = time.time()
        print u'{0} [{1}]'.format(contact_name, contact_id)
        
    def upsert_chatroom(self, data):
        room_id = data['UserName']
        if room_id not in self.chatroom:
            self.chatroom[room_id] = {}
            self.chatroom[room_id]['MemberList'] = {}
        self.chatroom[room_id]['EncryChatRoomId'] = data['EncryChatRoomId']
        self.chatroom[room_id]['HeadImgUrl'] = data['HeadImgUrl']
        self.chatroom[room_id]['NickName'] = data['NickName']

        print '>' * 40
        print data['NickName'] + ' [' + room_id + ']'

        for member in data['MemberList']:
            member_id = member['UserName']
            self.chatroom[room_id]['MemberList'][member_id] = member
            print u'\t- {0} [{1}]'.format(member['NickName'], member_id)

        print '<' * 40
        self.chatroom_timestamp[room_id] = time.time()
    
    def get_contact(self, contact_id):
        return self.contact.get(contact_id, None)
    
    def get_chatroom(self, room_id):
        return self.chatroom.get(room_id, None)

    def get_contact_age(self):
        return time.time() - self.contact_timestamp

    def get_chatroom_age(self, room_id):
        return time.time() - self.contact_timestamp.get(room_id, 0)
