import unittest
from unittest.mock import patch, MagicMock
from recipe.models.account_management_model import login, create_account, change_password, hash_password


class TestAccountManagementModel(unittest.TestCase):

    @patch('recipe.models.account_management_model.get_db_connection')
    def test_login_success(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value
        mock_get_db_connection.return_value.__enter__.return_value = mock_conn

        mock_cursor.fetchone.return_value = ('hashed_password',)
        with patch('recipe.models.account_management_model.hash_password', return_value='hashed_password'):
            self.assertTrue(login('test_user', 'test_password'))

    @patch('recipe.models.account_management_model.get_db_connection')
    def test_login_user_not_found(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchone.return_value = None
        mock_get_db_connection.return_value.__enter__.return_value = mock_conn

        with self.assertRaises(ValueError):
            login('nonexistent_user', 'password123')

    def test_create_account_invalid_username(self):
        with self.assertRaises(ValueError):
            create_account(None, 'password123')

    def test_create_account_invalid_password(self):
        with self.assertRaises(ValueError):
            create_account('valid_user', None)

    @patch('recipe.models.account_management_model.get_db_connection')
    def test_change_password_success(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchone.return_value = ('hashed_password',)
        mock_get_db_connection.return_value.__enter__.return_value = mock_conn

        with patch('recipe.models.account_management_model.hash_password',
                   side_effect=['hashed_password', 'new_hashed_password']):
            change_password('test_user', 'current_password', 'new_password')

    def test_hash_password(self):
        password = "mypassword"
        hashed = hash_password(password)
        self.assertIn('$', hashed)
