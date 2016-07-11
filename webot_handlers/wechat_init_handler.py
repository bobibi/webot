import pprint as pp


def wechat_init(context, msg):
        pp.pprint(msg)
        context.my_profile['Name'] = msg['User']['NickName']
        context.my_profile['Id'] = msg['User']['UserName']
