from dataclasses import dataclass
from typing import List
import logging
import os
import sqlite3

from recipe.utils.recipe_api_utils import fetch_recipes_from_api, fetch_trending_recipes

from recipe.utils.logger import configure_logger
from recipe.utils.random_utils import get_random
from recipe.utils.sql_utils import get_db_connection


logger = logging.getLogger(__name__)
configure_logger(logger)


@dataclass
class Recipe:
    id: int
    title: str
    ingredients: List[str]
    calories: int
     
    def __init__(self, title: str, url: str, ingredients: List[str], calories: int, diet_labels: str):
        self.title = title
        self.ingredients = ingredients
        self.calories = calories

def serach_recipes(ingredients, diet=None, calories=None) -> List[Recipe]:
    """
    Searches for recipe that satisfies the three parameters.
    
    Args:
        ingredients (str): Ingredients that must me included in the meal
        diet (str): Dietary restriction
        calories (str): The range of calories
    
    Returns:
        list: A list of recipes matching the search criteria.        
    """
    try:
        recipes = fetch_recipes_from_api(ingredients, diet, calories)
        return recipes
    except Exception as e:
        logger.error(f'Fails during API call: {e}')
        return []

def get_trending_recipes():
    """
    Retrieves a list of trending recipes.

    Returns:
        List[Recipe]: A list of trending Recipe objects.
    """
    try:
        return fetch_trending_recipes()
    except Exception as e:
        print(f"Error fetching trending recipes: {e}")
        return []