import logging

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
__SH = logging.StreamHandler()
__SH.setLevel(logging.INFO)
LOGGER.addHandler(__SH)
