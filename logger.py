import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import pytz


class BeijingFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, pytz.timezone('Asia/Shanghai'))
        if datefmt:
            return dt.strftime(datefmt)
        return dt.strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]


def setup_logger(name: str, log_file: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    handler = RotatingFileHandler(
        log_file, maxBytes=2 * 1024 * 1024, backupCount=5
    )
    formatter = BeijingFormatter('%(asctime)s - %(levelname)s - %(thread)d - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger