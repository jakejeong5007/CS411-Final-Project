import unittest
from unittest.mock import patch, MagicMock
from app import app

class TestApp(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    ####################################################
    # Health Checks
    ####################################################

    def test_healthcheck(self):
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'healthy'})

    @patch('recipe.utils.sql_utils.check_database_connection')
    @patch('recipe.utils.sql_utils.check_table_exists')
    def test_db_check_success(self, mock_check_table, mock_check_db):
        response = self.client.get('/api/db-check')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'database_status': 'healthy'})

    @patch('recipe.utils.sql_utils.check_database_connection', side_effect=Exception('DB error'))
    def test_db_check_failure(self, mock_check_db):
        response = self.client.get('/api/db-check')
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json)

    ####################################################
    # User Management
    ####################################################

    @patch('recipe.models.account_management_model.login')
    def test_login_success(self, mock_login):
        mock_login.return_value = True
        response = self.client.post('/api/login', json={'user_name': 'test', 'user_password': 'password'})
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json['login_status'])

    def test_login_missing_fields(self):
        response = self.client.post('/api/login', json={})
        self.assertEqual(response.status_code, 400)

    @patch('recipe.models.account_management_model.create_account')
    def test_create_account_success(self, mock_create_account):
        response = self.client.post('/api/create-account', json={'user_name': 'test', 'user_password': 'password'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['status'], 'success')

    def test_create_account_missing_fields(self):
        response = self.client.post('/api/create-account', json={})
        self.assertEqual(response.status_code, 400)

    ####################################################
    # Password Management
    ####################################################

    @patch('recipe.models.account_management_model.change_password')
    def test_update_password_success(self, mock_change_password):
        response = self.client.patch('/api/update-password', json={
            'user_name': 'test',
            'current_user_password': 'current',
            'new_user_password': 'new'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['status'], 'success')

    def test_update_password_missing_fields(self):
        response = self.client.patch('/api/update-password', json={})
        self.assertEqual(response.status_code, 400)

    ####################################################
    # Recipe Management
    ####################################################

    @patch('recipe.models.recipe_model.search_recipes')
    def test_search_recipes_success(self, mock_search):
        mock_search.return_value = []
        response = self.client.get('/api/search?ingredients=chicken')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['recipes'], [])

    def test_search_recipes_missing_ingredients(self):
        response = self.client.get('/api/search')
        self.assertEqual(response.status_code, 400)

    @patch('recipe.models.recipe_model.get_trending_recipes')
    def test_trending_recipes_success(self, mock_trending):
        mock_trending.return_value = []
        response = self.client.get('/api/trending')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['recipes'], [])

    @patch('recipe.models.recipe_account_model.update_preferences')
    def test_update_preferences_success(self, mock_update):
        response = self.client.put('/api/preferences', json={'preferences': ('chicken', 500, 'keto')})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['preferences'], ('chicken', 500, 'keto'))

    def test_update_preferences_missing_fields(self):
        response = self.client.put('/api/preferences', json={})
        self.assertEqual(response.status_code, 500)

    @patch('recipe.models.recipe_account_model.get_user_preferences')
    def test_get_preferences_success(self, mock_get_preferences):
        mock_get_preferences.return_value = ('chicken', 500, 'keto')
        response = self.client.get('/api/get-preferences')
        self.assertEqual(response.status_code, 200)

    def test_save_recipe_missing_fields(self):
        response = self.client.post('/api/saveRecipe', json={})
        self.assertEqual(response.status_code, 400)
