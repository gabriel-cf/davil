import logging

class Logger(object):
    """Single logger used across the application"""
    # Logging level across the whole application
    LEVEL = logging.DEBUG

    @staticmethod
    def init_logging():
        logging.basicConfig(format='%(asctime)s\t%(levelname)s\t%(name)s\t%(message)s', level=Logger.LEVEL)
        logging.info('Logging started')
