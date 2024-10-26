import logging
import logging.handlers
from datetime import datetime, timedelta

class BeijingFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created)
        dt_beijing = dt + timedelta(hours=8)
        if datefmt:
            return dt_beijing.strftime(datefmt)
        return dt_beijing.strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]

def setup_logger(name: str, log_file: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=2*1024*1024, backupCount=5
    )
    formatter = BeijingFormatter('%(asctime)s - %(levelname)s - %(thread)d - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger