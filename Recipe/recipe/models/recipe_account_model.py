import logging
import json
from typing import List, Optional, Tuple

from recipe.utils.sql_utils import get_db_connection, sqlite3
from recipe.utils.logger import configure_logger
from recipe.models.recipe_model import Recipe
from recipe.utils.recipe_api_utils import fetch_recipes_from_api

logger = logging.getLogger(__name__)
configure_logger(logger)

class RecipeAccountModel:
  """
  A class to manage recipes of a user's account.

  Attributes:
      prev_ingredient (Optional[str]): The preferred main ingredient.
      pref_calorie (Optional[int]): The preferred calorie limit.
      pref_diet (Optional[str]): The preferred diet type.
      favorites (List[Recipe]): The list of favorite recipes.
  """

  def __init__(self):
      """
      Initializes the RecipeAccountModel with empty preferences and an empty favorites list.
      """
      self.prev_ingredient: Optional[str] = None
      self.pref_calorie: Optional[int] = None
      self.pref_diet: Optional[str] = None
      self.favorites: List[Recipe] = []

  def get_user_preferences(self) -> Tuple[Optional[str], Optional[int], Optional[str]]:
      """
      Retrieves the user's current preferences.

      Returns:
          Tuple[Optional[str], Optional[int], Optional[str]]: 
          A tuple containing the preferred ingredient, calories, and diet.
      """
      logger.info("Retrieving user preferences")
      return self.prev_ingredient, self.pref_calorie, self.pref_diet

  def recommend_recipes(self, preferences: Optional[Tuple[Optional[str], Optional[int], Optional[str]]], cuisine: str) -> List[Recipe]:
    """
    Recommends recipes based on user preferences and cuisine.

    Args:
        preferences (Tuple[Optional[str], Optional[int], Optional[str]]): 
            The user's preferences (ingredient, calorie limit, diet).
        cuisine (str): The preferred cuisine type.

    Returns:
        List[Recipe]: A list of recommended recipes matching the criteria.
    """
    logger.info("Recommending recipes based on preferences and cuisine")
    ingredient, calorie_limit, diet = preferences

    # Prepare calorie range string for the API
    calorie_range = f"0-{calorie_limit}" if calorie_limit else None

    # Fetch recipes from the Edamam API
    try:
        recipes = fetch_recipes_from_api(
            ingredients=ingredient,
            diet=diet,
            calories=calorie_range,
            cuisine=cuisine
        )
    except Exception as e:
        logger.error("Error fetching recipes from the API: %s", e)
        return []

    # Further filter recipes to match cuisine (if not already used as ingredients)
    filtered_recipes = [
        recipe for recipe in recipes
        if cuisine.lower() in recipe.title.lower() or cuisine.lower() in recipe.ingredients
    ]

    logger.info("Found %d recommended recipes", len(filtered_recipes))
    return filtered_recipes


  def save(self, recipe_id: int) -> None:
      """
      Saves a recipe to the user's favorites by its ID.

      Args:
          recipe_id (int): The ID of the recipe to save.

      Raises:
          TypeError: If the recipe_id is not a valid integer.
          ValueError: If the recipe is already in favorites or does not exist.
      """
      logger.info("Saving a recipe to favorites by ID: %d", recipe_id)

      if not isinstance(recipe_id, int):
          logger.error("Invalid recipe ID type")
          raise TypeError("The provided recipe ID must be an integer.")

      # Fetch recipe from database
      try:
          with get_db_connection() as conn:
              cursor = conn.cursor()
              cursor.execute("SELECT title, ingredients, calories FROM recipes WHERE id = ?", (recipe_id,))
              result = cursor.fetchone()

              if not result:
                  logger.error("Recipe with ID %d does not exist", recipe_id)
                  raise ValueError(f"Recipe with ID {recipe_id} does not exist.")

              # Convert the fetched data into a Recipe object
              recipe = Recipe(
                  title=result[0],
                  ingredients=json.loads(result[1]),
                  calories=result[2]
              )

              # Check if the recipe is already in favorites
              if recipe in self.favorites:
                  logger.error("Recipe with ID %d is already in favorites", recipe_id)
                  raise ValueError(f"Recipe with ID {recipe_id} is already in the favorites list.")

              # Add to favorites
              self.favorites.append(recipe)
              logger.info("Recipe '%s' has been added to favorites", recipe.title)

      except sqlite3.Error as e:
          logger.error("Database error while fetching recipe: %s", str(e))
          raise sqlite3.Error(f"Database error: {str(e)}")


  def update_preferences(self, preferences: Tuple[Optional[str], Optional[int], Optional[str]]) -> None:
      """
      Updates the user's preferences.

      Args:
          preferences (Tuple[Optional[str], Optional[int], Optional[str]]): 
              A tuple containing the preferred ingredient, calories, and diet.
      """
      logger.info("Updating user preferences")
      if len(preferences) != 3 or not isinstance(preferences[0], (str, type(None))) or not isinstance(preferences[1], (int, type(None))) or not isinstance(preferences[2], (str, type(None))):
          logger.error("Invalid preferences format")
          raise ValueError("Preferences must be a tuple with (Optional[str], Optional[int], Optional[str]).")

      self.prev_ingredient, self.pref_calorie, self.pref_diet = preferences
      logger.info("Preferences updated to: ingredient=%s, calories=%s, diet=%s", self.prev_ingredient, self.pref_calorie, self.pref_diet)
