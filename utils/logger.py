import logging
from logging.handlers import RotatingFileHandler

def Setup_logging(log_file):
    
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.DEBUG)

    formmater = logging.Formatter(fmt='%(asctime)s | %(levelname)s | %(name)s | %(funcName)s | %(message)s', 
                                  datefmt='%Y-%m-%d %H:%M:%S',)

    file_Handler = RotatingFileHandler(filename=log_file, mode='a', 
                                       maxBytes=5*1024*1024, backupCount=3)
    file_Handler.setFormatter(fmt=formmater)
    file_Handler.setLevel(level=logging.DEBUG)

    console_Handler = logging.StreamHandler()
    console_Handler.setFormatter(fmt=formmater)
    console_Handler.setLevel(level=logging.INFO)
    
    logger.addHandler(file_Handler)
    logger.addHandler(console_Handler)
    
    if logger.handlers:
        return logger

if __name__ == '__main__':
    logger = Setup_logging('logs/test_logs/test_logs.log')
    logger.info('Testing the logger, INFO Level')
    logger.debug('This DEBUG Message')
    logger.warning('This is Warning message')
    logger.error('This is Error Message')
    logger.critical('This is Critical Error')

