import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging(
    log_file,
    log_level=logging.DEBUG,
    console_level=logging.INFO,
    max_bytes=5 * 1024 * 1024,
    backup_count=3,
    encoding='utf-8',):

    logger = logging.getLogger()
    logger.setLevel(log_level)

    if logger.handlers:
        return logger

    log_dir = os.path.dirname(log_file)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)s | %(module)s | %(pathname)s:%(lineno)d | %(name)s | %(funcName)s | %(message)s' ,
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    file_handler = RotatingFileHandler(
        filename=log_file,
        mode='a',
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding=encoding,
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(console_level)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


if __name__ == '__main__':
    logger = setup_logging('logs/test_logs/test_logs.log')
    logger.info('Testing the logger, INFO Level')
    logger.debug('This DEBUG Message')
    logger.warning('This is Warning message')
    logger.error('This is Error Message')
    logger.critical('This is Critical Error')

