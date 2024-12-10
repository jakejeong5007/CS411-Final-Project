import unittest
from unittest.mock import patch, MagicMock
from recipe.models.recipe_model import search_recipes, save_recipes, get_trending_recipes

class TestRecipeModel(unittest.TestCase):

    @patch('recipe.models.recipe_model.fetch_recipes_from_api')
    def test_search_recipes_valid(self, mock_fetch):
        mock_fetch.return_value = []
        self.assertEqual(search_recipes('chicken'), [])

    @patch('recipe.models.recipe_model.fetch_recipes_from_api')
    def test_search_recipes_invalid(self, mock_fetch):
        mock_fetch.side_effect = Exception('API Error')
        self.assertEqual(search_recipes('invalid'), [])

    @patch('recipe.models.recipe_model.fetch_trending_recipes')
    def test_get_trending_recipes(self, mock_fetch):
        mock_fetch.return_value = []
        self.assertEqual(get_trending_recipes(), [])
