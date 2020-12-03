import logging
import os

LOG_DIR = './logs'
LOG_FMT = '%(asctime)s - %(name)s - [%(levelname)s] %(message)s'

LOGGER = logging.getLogger('helpers')
LOGGER.setLevel(logging.DEBUG)

os.makedirs(LOG_DIR, exist_ok=True)
__FH = logging.FileHandler(f'{LOG_DIR}/test.log')
__FH.setLevel(logging.DEBUG)
__FH.setFormatter(logging.Formatter(LOG_FMT))
LOGGER.addHandler(__FH)
