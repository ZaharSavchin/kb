from loguru import logger

logger.add('loguru.log',
           format='{time} {level} {message}',
           level='INFO',
           rotation='2 mb',
           compression='zip')
