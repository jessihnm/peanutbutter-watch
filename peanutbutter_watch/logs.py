import logging
import coloredlogs


def get_logger(*args, **kw):
    logger = logging.getLogger(*args, **kw)
    coloredlogs.install(level="DEBUG", logger=logger)
    return logger
