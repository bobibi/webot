import pprint as pp


def contact_package_handler(context, msg):
    print '{0} contacts fetched!'.format(msg['MemberCount'])
    for ct in msg['MemberList']:
        single_contact_handler(context, ct)


def single_contact_handler(context, contact):
    context['contact'][contact['UserName']] = contact
