import logging

from logging.handlers import RotatingFileHandler

def app_logger():
    
    log_date = '%Y-%m-%d %H:%M:%S'
    log_format = '%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'
    handler = RotatingFileHandler('logs/app.log', maxBytes=100000, backupCount=1)
    formatter = logging.Formatter(log_format, log_date)
    handler.setFormatter(formatter)
    handler.suffix = f'%Y-%m-%d.log'
    handler.setLevel(logging.INFO)

    logger = logging.getLogger('fwmig')
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger
