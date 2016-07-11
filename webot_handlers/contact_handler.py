import pprint as pp
import logging


def contact_package_handler(context, msg):
    logging.info('{0} contacts fetched!'.format(msg['MemberCount']))
    for ct in msg['MemberList']:
        context.upsert_contact(ct)
