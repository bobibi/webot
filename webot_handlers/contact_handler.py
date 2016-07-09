import pprint as pp


def contact_package_handler(context, msg):
    print '{0} contacts fetched!'.format(msg['MemberCount'])
    for ct in msg['MemberList']:
        context.upsert_contact(ct)
