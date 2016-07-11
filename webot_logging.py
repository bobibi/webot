import logging

log_file = 'webot.log'
log_level = logging.INFO


def init():
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.basicConfig(filename=log_file, level=log_level, format='%(asctime)s [%(levelname)s] %(message)s')
