import unittest
import logging
from recipe.utils.logger import configure_logger

class TestLogger(unittest.TestCase):

    def test_logger_configuration(self):
        logger = logging.getLogger('test_logger')
        configure_logger(logger)
        self.assertEqual(len(logger.handlers), 1)
