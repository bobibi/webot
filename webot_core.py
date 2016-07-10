import string, random, requests, re, urllib, time, cStringIO, json, logging


class WebotCore(object):

    def __init__(self):
        self.uuid = None
        self.wxuin = None
        self.wxsid = None
        self.deviceid = 'e' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '\
                          'Chrome/47.0.2526.106 Safari/537.36'
        self.qr_url = None

    def start(self, res_hanlder, context):
        self.get_uuid()
        logging.info(self.qr_url)
        remain_check = 10
        while not self.check_login() and remain_check > 0:
            remain_check -= 1
            logging.info('Please scan the QR using your wechat client: {url}'.format(url=self.qr_url))
            logging.info('checking remaining: {0}'.format(remain_check))

        init_res = self.wechat_init()
        res_hanlder.wechat_init(context, init_res)

        contact_res = self.get_contact()
        res_hanlder.wechat_contact(context, contact_res)

        # TODO: capture signal routines when process shutdown
        while True:
            sync_res = self.synccheck()
            res_hanlder.wechat_sync(context, sync_res)

            msg_res = self.fetch_message()
            task_pool = res_hanlder.wechat_message(context, msg_res)

            for out_msg in task_pool.out_messages:
                self.send_message(out_msg['to'], out_msg['msg'])

            if len(task_pool.chatrooms_need_info) > 0:
                chatroom_res = self.get_chatrooms_info(task_pool.chatrooms_need_info)
                res_hanlder.wechat_chatroom_info(context, chatroom_res)

            if task_pool.refresh_contact:
                contact_res = self.get_contact()
                res_hanlder.wechat_contact(context, contact_res)

    def get_uuid(self):
        url = 'https://login.weixin.qq.com/jslogin?appid=wx782c26e4c19acffb&redirect_uri=https%3A%2F%2Fwx.qq.com'\
              '%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&fun=new&lang=zh_CN'
        r = requests.get(url)
        uuid_search = re.search('window.QRLogin.uuid = "([^"]+)"', r.text)
        self.uuid = uuid_search.group(1)
        self.qr_url = 'https://login.weixin.qq.com/qrcode/'+self.uuid

    def pop_qr(self):
        from PIL import Image
        if self.uuid is None:
            raise Exception('initialize uuid first!!')
        img = Image.open(cStringIO.StringIO(urllib.urlopen(self.qr_url).read()))
        img.show()

    def check_login(self):
        url = 'https://login.weixin.qq.com/cgi-bin/mmwebwx-bin/login?uuid='+self.uuid+'&tip=1'
        r = requests.get(url)
        url_search = re.search('window.redirect_uri="([^"]+)"', r.text)
        if url_search:
            url = url_search.group(1)
            r = requests.head(url)
            self.wxuin = r.cookies['wxuin']
            self.wxsid = r.cookies['wxsid']
            self.cookie = r.cookies
            return True
        return False

    def login_success(self):
        return self.wxuin is not None and self.wxsid is not None

    def wechat_init(self):
        if not self.login_success():
            raise Exception('login first!!')
        payload = {
            'BaseRequest': {
                'Uin': self.wxuin,
                'Sid': self.wxsid,
                'Skey': '',
                'DeviceID': self.deviceid,
            }
        }
        url = 'https://web2.wechat.com/cgi-bin/mmwebwx-bin/webwxinit'
        r = requests.post(url, json = payload, cookies=self.cookie)
        rjson = json.loads(r.content.decode('utf-8', 'replace'))

        self.user = rjson['User']
        self.skey = rjson['SKey']
        self.synckey = self.gen_synckey(rjson['SyncKey'])
        self.synckey_json = rjson['SyncKey']
        print 'Weixin init completed!\nUserName:%s\nNickName:%s\n'%(rjson['User']['UserName'], rjson['User']['NickName'])
        return rjson

    def gen_synckey(self, synckey):
        return '|'.join(['%d_%d'%(k,v) for L in synckey['List'] for v,k in [(L['Val'],L['Key'])]])

    def get_contact(self):
        url = 'https://web2.wechat.com/cgi-bin/mmwebwx-bin/webwxgetcontact'
        headers = {
            'ContentType': 'application/json; charset=UTF-8'
        }
        r = requests.post(url, json={'skey': self.skey}, cookies=self.cookie, headers=headers)
        data = r.content
        data = data.decode('utf-8', 'replace')
        dic = json.loads(data)
        return dic

    def synccheck(self):
        url = 'https://webpush2.wechat.com/cgi-bin/mmwebwx-bin/synccheck'
        params = {
            'sid': self.wxsid,
            'uin': self.wxuin,
            'deviceid': self.deviceid,
            'synckey': self.synckey,
        }
        r = requests.get(url, params=params, cookies=self.cookie)

        return r.text

    def fetch_message(self):
        url = 'https://web2.wechat.com/cgi-bin/mmwebwx-bin/webwxsync?sid=%s&skey=%s'%(self.wxsid, self.skey)
        data = {
            "BaseRequest" : {
                "Uin": self.wxuin,
                "Sid": self.wxsid,
            },
            "SyncKey" : self.synckey_json,
        }
        headers = {
            'ContentType': 'application/json; charset=UTF-8'
        }
        r = requests.post(url, json=data, cookies=self.cookie)
        data = r.content
        data = data.decode('utf-8', 'replace')
        dic = json.loads(data)

        self.synckey = self.gen_synckey(dic['SyncKey'])
        self.synckey_json = dic['SyncKey']

        return dic

    def gen_local_id(self):
        return int(time.time()*1000)

    def send_message(self, to, msg):
        url = 'https://web2.wechat.com/cgi-bin/mmwebwx-bin/webwxsendmsg'
        data = {
            u"BaseRequest":{
                u"DeviceID" : self.deviceid,
                u"Sid" : self.wxsid,
                u"Skey" : self.skey,
                u"Uin" : self.wxuin
            },
            u"Msg" : {
                u"ClientMsgId" : self.gen_local_id(),
                u"Content" : msg,
                u"FromUserName" : self.user[u'UserName'],
                u"LocalID" : self.gen_local_id(),
                u"ToUserName" : to,
                u"Type" : 1
            },
        }
        #print repr(data)
        headers = {
            'ContentType': 'application/json; charset=UTF-8'
        }
        r = requests.post(url, data=json.dumps(data, ensure_ascii=False).encode('utf-8'), cookies=self.cookie, headers=headers)
        #print r.text
        return r.text

    def get_chatrooms_info(self, usernames):
        url = 'https://web2.wechat.com/cgi-bin/mmwebwx-bin/webwxbatchgetcontact?type=ex'
        if not isinstance(usernames, list):
            usernames = [usernames]
        data = {
            "BaseRequest":{
                "Uin": self.wxuin,
                "Sid": self.wxsid,
                "Skey": self.skey,
                "DeviceID": self.deviceid
            },
            "Count": len(usernames),
            "List":[{"UserName": un, "EncryChatRoomId":""} for un in usernames]
        }
        r = requests.post(url, json = data, cookies=self.cookie)
        rjson = json.loads(r.content.decode('utf-8', 'replace'))
        return rjson
