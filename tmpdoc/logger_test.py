import logging


logging.basicConfig(level=logging.WARNING, filename='test.log')

logger1 = logging.getLogger('package1')
logger2 = logging.getLogger('package2')

logger1.warning('This message comes from one module')
logger2.warning('And this message comes from another module')

logger1.info('I told you so')
