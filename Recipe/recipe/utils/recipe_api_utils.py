import logging
import requests

from typing import List

from recipe.utils.logger import configure_logger
from recipe.models.recipe_model import Recipe

logger = logging.getLogger(__name__)
configure_logger(logger)

app_id = "APP_ID"
app_key = "APP_KEY"
base_url = "https://api.edamam.com/api/recipes/v2"


def fetch_recipes_from_api(ingredients, diet=None, calories=None) -> List[Recipe]:
    """
    Calls the Edamam API to search for recipes based on the provided parameters.

    Args:
        ingredients (str): Ingredients that must be included in the meal.
        diet (str, optional): Dietary restriction.
        calories (str, optional): The range of calories.

    Returns:
        list: A list of matching recipes with details.
    """

    params = {
        "type": "public",
        "q": ingredients,
        "app_id": app_id,
        "app_key": app_key,
    }

    if diet:
        params["diet"] = diet
    if calories:
        params["calories"] = calories

    response = requests.get(base_url, params=params)
    response.raise_for_status()  # Raise an error for bad HTTP responses

    data = response.json()
    recipes = []

    for hit in data.get("hits", []):
        recipe_data = hit.get("recipe", {})
        recipe = Recipe(
            title=recipe_data.get("label", "No Title"),
            ingredients=recipe_data.get("ingredientLines", []),
            calories=int(recipe_data.get("calories", 0))
        )
        recipes.append(recipe)

    return recipes

def fetch_trending_recipes() -> List[Recipe]:
    """
    Fetches trending recipes from the Edamam API.

    Returns:
        List[Recipe]: A list of trending Recipe objects.
    """

    # Example criteria for trending recipes (e.g., popular dishes like "pizza", "pasta", etc.)
    trending_keywords = ["pizza", "pasta", "burger", "salad", "chocolate"]
    recipes = []

    for keyword in trending_keywords:
        params = {
            "type": "public",
            "q": keyword,
            "app_id": app_id,
            "app_key": app_key,
        }

        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an error for bad HTTP responses

        data = response.json()

        for hit in data.get("hits", []):
            recipe_data = hit.get("recipe", {})
            recipe = Recipe(
                title=recipe_data.get("label", "No Title"),
                ingredients=recipe_data.get("ingredientLines", []),
                calories=int(recipe_data.get("calories", 0)),
            )
            recipes.append(recipe)

    return recipes
