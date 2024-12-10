import unittest
from recipe.models.recipe_account_model import RecipeAccountModel

class TestRecipeAccountModel(unittest.TestCase):

    def test_get_user_preferences_empty(self):
        model = RecipeAccountModel()
        self.assertEqual(model.get_user_preferences(), (None, None, None))

    def test_update_preferences(self):
        model = RecipeAccountModel()
        model.update_preferences(('chicken', 500, 'keto'))
        self.assertEqual(model.get_user_preferences(), ('chicken', 500, 'keto'))

    def test_update_preferences_invalid(self):
        model = RecipeAccountModel()
        with self.assertRaises(ValueError):
            model.update_preferences(('chicken', 'invalid', 'keto'))
