import logging


def init():
    logging.basicConfig(filename='myapp.log', level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
