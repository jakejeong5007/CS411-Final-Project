import logging
import requests

from recipe.utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)

app_id = "APP_ID"
app_key = "APP_KEY"


def get_random(num_songs: int) -> int:
    """
    Fetches a random int between 1 and the number of songs in the catalog from random.org.

    Returns:
        int: The random number fetched from random.org.

    Raises:
        RuntimeError: If the request to random.org fails or returns an invalid response.
        ValueError: If the response from random.org is not a valid float.
    """
    url = f"https://www.random.org/integers/?num=1&min=1&max={num_songs}&col=1&base=10&format=plain&rnd=new"

    try:
        # Log the request to random.org
        logger.info("Fetching random number from %s", url)

        response = requests.get(url, timeout=5)

        # Check if the request was successful
        response.raise_for_status()

        random_number_str = response.text.strip()

        try:
            random_number = int(random_number_str)
        except ValueError:
            raise ValueError("Invalid response from random.org: %s" % random_number_str)

        logger.info("Received random number: %.3f", random_number)
        return random_number

    except requests.exceptions.Timeout:
        logger.error("Request to random.org timed out.")
        raise RuntimeError("Request to random.org timed out.")

    except requests.exceptions.RequestException as e:
        logger.error("Request to random.org failed: %s", e)
        raise RuntimeError("Request to random.org failed: %s" % e)

def get_recipes(query, app_id, app_key, calories=None):
    url = 'https://api.edamam.com/api/recipes/v2'
    params = {
        'type': 'public',
        'q': query,
        'app_id': app_id,
        'app_key': app_key,
    }
    if calories:
        params['calories'] = calories
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
        
def fetch_recipes_from_api(ingredients, diet=None, calories=None):
    """
    Calls the Edamam API to search for recipes based on the provided parameters.

    Args:
        ingredients (str): Ingredients that must be included in the meal.
        diet (str, optional): Dietary restriction.
        calories (str, optional): The range of calories.

    Returns:
        list: A list of matching recipes with details.
    """

    base_url = "https://api.edamam.com/api/recipes/v2"

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
        recipe = hit.get("recipe", {})
        recipes.append({
            "label": recipe.get("label"),
            "url": recipe.get("url"),
            "ingredients": recipe.get("ingredientLines"),
            "calories": recipe.get("calories"),
            "diet_labels": recipe.get("dietLabels"),
        })

    return recipes
