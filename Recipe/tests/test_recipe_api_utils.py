import unittest
from unittest.mock import patch
from recipe.utils.recipe_api_utils import fetch_recipes_from_api

class TestRecipeAPIUtils(unittest.TestCase):

    @patch('requests.get')
    def test_fetch_recipes_from_api_success(self, mock_get):
        mock_get.return_value.json.return_value = {'hits': []}
        recipes = fetch_recipes_from_api('test')
        self.assertEqual(recipes, [])

    @patch('requests.get')
    def test_fetch_recipes_from_api_failure(self, mock_get):
        mock_get.side_effect = Exception('API error')
        with self.assertRaises(Exception):
            fetch_recipes_from_api('invalid')
