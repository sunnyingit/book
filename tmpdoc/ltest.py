# -*- conding: utf-8 -*-

import logging

LOG_FILENAME = '/tmp/logging_example.out'

logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.DEBUG,
                    )

logging.debug('This message should go to the log file')
logging.info('This message should go to the log file')
