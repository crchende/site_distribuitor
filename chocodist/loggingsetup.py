from .params import APPNAME

import logging
logger = logging.getLogger(APPNAME)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter(\
    fmt='[%(asctime)s]: %(levelname)s: %(name)s: %(funcName)s: %(message)s')
    #, \
    #datefmt="%y-%m-%d %H:%M:%S %f") # milisecundele se afiseaza default iar formatarea este ca in datefmt
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)