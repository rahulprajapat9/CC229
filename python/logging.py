import logging

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="test.log",
                    level = logging.ERROR,
                    format=LOG_FORMAT,
                    filemode='w')
logger = logging.getLogger()

logging.debug('debug message')
logging.info('info message')
logging.warning('warning message')
logging.error('error message')
logging.critical('critical message')

print logger.level