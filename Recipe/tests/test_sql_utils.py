import unittest
from unittest.mock import patch
from recipe.utils.sql_utils import check_database_connection

class TestSQLUtils(unittest.TestCase):

    @patch('sqlite3.connect')
    def test_check_database_connection_success(self, mock_connect):
        check_database_connection()
        mock_connect.assert_called_once()

    @patch('sqlite3.connect')
    def test_check_database_connection_failure(self, mock_connect):
        mock_connect.side_effect = Exception('DB error')
        with self.assertRaises(Exception):
            check_database_connection()
