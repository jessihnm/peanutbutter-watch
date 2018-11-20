import logging
import coloredlogs


def get_logger(*args, **kw):
    logger = logging.getLogger(*args, **kw)
    coloredlogs.install(level="INFO", logger=logger)
    return logger
