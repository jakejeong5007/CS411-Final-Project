import logging
from typing import List, Optional

from recipe.utils.logger import configure_logger
from recipe.models.recipe_model import Recipe

logger = logging.getLogger(__name__)
configure_logger(logger)

class RecipeAccountModel:
  """
  A class to manage recipes of a user's account.

  Attributes:
      pref_calories (Optional[int]): The preferred calorie limit.
      pref_diet (Optional[str]): The preferred diet type.
      favorites (List[Recipe]): The list of favorite recipes.
  """

  def __init__(self):
      """
      Initializes the RecipeAccountModel with empty preferences and an empty favorites list.
      """
      self.pref_calories: Optional[int] = None
      self.pref_diet: Optional[str] = None
      self.favorites: List[Recipe] = []

  def get_user_preferences(self) -> List[Optional[int, str]]:
      """
      Retrieves the user's current preferences.

      Returns:
          List[Optional[int, str]]: A list containing the preferred calories and diet.
      """
      logger.info("Retrieving user preferences")
      return [self.pref_calories, self.pref_diet]

  def recommend_recipes(self, preferences: List[Optional[int, str]], cuisine: str) -> List[Recipe]:
      """
      Recommends recipes based on user preferences and cuisine.

      Args:
          preferences (List[Optional[int, str]]): The user's preferences [calories, diet].
          cuisine (str): The preferred cuisine type.

      Returns:
          List[Recipe]: A list of recommended recipes matching the criteria.
      """


  def save(self, recipe: Recipe) -> None:
    """
    Saves a recipe to the user's favorites.

    Args:
      recipe (Recipe): The recipe to save.

    Raises:
      TypeError: If the recipe is not a valid Recipe instance.
      ValueError: If the recipe is already in favorites.
    """
    logger.info("Saving a recipe to favorites")
    if not isinstance(recipe, Recipe):
      logger.error("Invalid recipe type")
      raise TypeError("The provided recipe is not a valid Recipe instance.")

    if recipe in self.favorites:
      logger.error("Recipe is already in favorites")
      raise ValueError("This recipe is already in the favorites list.")

    self.favorites.append(recipe)
    logger.info("Recipe '%s' has been added to favorites", recipe.title)

  def update_preferences(self, preferences: List[Optional[int, str]]) -> None:
    """
    Updates the user's preferences.

    Args:
      preferences (List[Optional[int, str]]): A list containing preferred calories and diet.
    """
    logger.info("Updating user preferences")
    if len(preferences) != 2 or not isinstance(preferences[0], (int, type(None))) or not isinstance(preferences[1], (str, type(None))):
        logger.error("Invalid preferences format")
        raise ValueError("Preferences must be a list with [Optional[int], Optional[str]].")

    self.pref_calories, self.pref_diet = preferences
    logger.info("Preferences updated to: calories=%s, diet=%s", self.pref_calories, self.pref_diet)