from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, Response, request

from recipe.models import recipe_account_model, recipe_model, account_management_model
from recipe.utils.sql_utils import check_database_connection, check_table_exists

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)



####################################################
#
# Healthchecks
#
####################################################

@app.route('/api/health', methods=['GET'])
def healthcheck() -> Response:
    """
    Health check route to verify the service is running.

    Returns:
        JSON response indicating the health status of the service.
    """
    app.logger.info('Health check')
    return make_response(jsonify({'status': 'healthy'}), 200)


@app.route('/api/db-check', methods=['GET'])
def db_check() -> Response:
    """
    Route to check if the database connection and users table are functional.

    Returns:
        JSON response indicating the database health status.
    Raises:
        404 error if there is an issue with the database.
    """
    try:
        app.logger.info("Checking database connection...")
        check_database_connection()
        app.logger.info("Database connection is OK.")
        app.logger.info("Checking if user table exists...")
        check_table_exists("users")
        app.logger.info("users table exists.")
        return make_response(jsonify({'database_status': 'healthy'}), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 404)


##########################################################
#
# Password Management
#
##########################################################

@app.route('/api/login', methods=['POST'])
def login() -> Response:
    """
    Route to check if provided password exists in database

    Expected JSON Input:
        - user_name (str): The user name for account
        - user_password (str): The password for account

    Returns:
        JSON response indicating the success of the login
    Raises:
        400 error if input validation fails
        500 error if there is an issue during login
    """
    app.logger.info('Login attempt start')
    try:
        data = request.get_json()

        user_name = data.get('user_name')
        user_password = data.get('user_password')
        if not user_name or not user_password:
            return make_response(jsonify({'error': 'Invalid input, all fields are required with valid values'}), 400)

        app.logger.info('Validating given password for: %s', user_name)
        login_res = account_management_model.login(user_name, user_password)
        app.logger.info('Password check completed for: %s', user_name)
        return make_response(jsonify({'status': 'success', 'user_name': user_name, 'login_status': login_res}), 201)
    except Exception as e:
        app.logger.error('Failed to check password')
        return make_response(jsonify({'error': str(e)}), 500)


@app.route('/api/create-account', methods=['POST'])
def create_account() -> Response:
    """
    Route to create a new user account

    Expected JSON Input:
        - user_name (str): The user name for account
        - user_password (str): The password for account

    Returns:
        JSON response indicating the success of creating the account
    Raises:
        400 error if input validation fails
        500 error if there is an issue creating user account
    """
    app.logger.info('Creating account')
    try:
        data = request.get_json()

        user_name = data.get('user_name')
        user_password = data.get('user_password')

        if not user_name or not user_password:
            return make_response(jsonify({'error': 'Invalid input, all fields are required with valid values'}), 400)

        app.logger.info('Creating account')
        account_management_model.create_account(user_name, user_password)
        app.logger.info('Account created')
        return make_response(jsonify({'status': 'success', 'user_name': user_name}), 201)
    except Exception as e:
        app.logger.error('Failed to create account')
        return make_response(jsonify({'error': str(e)}), 500)


@app.route('/api/update-password', methods=['PATCH'])
def update_password() -> Response:
    """
    Route to update password for user account

    Expected JSON Input:
        - user_name (str): The user name for account
        - current_user_password (str): The current user password
        - new_user_password (str): The password the user wants to update to

    Returns:
        JSON reponse indicating the success of creating the accoutn
    Raises:
        400 error if input validation fails
        500 error if there is an issue updating user password
    """
    app.logger.info('Updating user password')

    try:
        data = request.get_json()

        user_name = data.get('user_name')
        current_user_password = data.get('current_user_password')
        new_user_password = data.get('new_user_password')

        if not user_name or not current_user_password or not new_user_password:
            return make_response(jsonify({'error': 'Invalid input, all fields are required with valid values'}), 400)

        app.logger.info('Updating password')
        account_management_model.change_password(user_name, current_user_password, new_user_password)
        app.logger.info('Password updated')
        return make_response(jsonify({'status': 'success', 'user_name': user_name}), 201)
    except Exception as e:
        app.logger.error('Failed to update password')
        return make_response(jsonify({'error': str(e)}), 500)


##########################################################
#
# Recipe Management
#
##########################################################

@app.route('/api/search', methods=['GET'])
def search() -> Response:
    """
    Route to search for recipes by ingredients.

    Query Parameters:
        - ingredients (str): Comma-separated list of ingredients (required).
        - diet (str, optional): Dietary restriction (e.g., vegan, keto).
        - calories (str, optional): Calorie range (e.g., 200-400).

    Returns:
        JSON response with search results or an error message.
    """
    try:
        ingredients = request.args.get('ingredients')
        diet = request.args.get('diet')
        calories = request.args.get('calories')

        if not ingredients:
            return make_response(jsonify({'error': 'Ingredients parameter is required'}), 400)

        app.logger.info("Searching recipes with ingredients: %s, diet: %s, calories: %s", ingredients, diet, calories)

        # Fetch recipes using the utility function
        recipes = recipe_model.search_recipes(ingredients=ingredients, diet=diet, calories=calories)
        return make_response(jsonify({'status': 'success', 'recipes': recipes}), 200)
    except Exception as e:
        app.logger.error("Error searching for recipes: %s", str(e))
        return make_response(jsonify({'error': str(e)}), 500)


@app.route('/api/recommend', methods=['GET'])
def recommend() -> Response:
    """
    Route to get personalized recipe recommendations.

    Query Parameters:
        - userId (str): User ID (required).
        - cuisine (str, optional): Preferred cuisine type.

    Returns:
        JSON response with recommended recipes or an error message.
    """
    try:

        cuisine = request.args.get('cuisine')

        app.logger.info("Fetching recommendations for, cuisine: %s", cuisine)

        # Fetch user preferences and recommend recipes
        preferences = recipe_account_model.get_user_preferences()
        if not preferences:
            return make_response(jsonify({'error': 'User preferences not found'}), 404)

        recipes = recipe_model.recommend_recipes(preferences, cuisine=cuisine)
        return make_response(jsonify({'status': 'success', 'recipes': recipes}), 200)
    except Exception as e:
        app.logger.error("Error recommending recipes: %s", str(e))
        return make_response(jsonify({'error': str(e)}), 500)


@app.route('/api/trending', methods=['GET'])
def trending() -> Response:
    """
    Route to view trending recipes.

    Returns:
        JSON response with trending recipes or an error message.
    """
    try:
        app.logger.info("Fetching trending recipes")

        # Fetch trending recipes from the model
        trending_recipes = recipe_model.get_trending_recipes()
        return make_response(jsonify({'status': 'success', 'recipes': trending_recipes}), 200)
    except Exception as e:
        app.logger.error("Error fetching trending recipes: %s", str(e))
        return make_response(jsonify({'error': str(e)}), 500)


@app.route('/api/saveRecipe', methods=['POST'])
def save() -> Response:
    """
    Saves recipes to a user's profile

    Expected JSON Input:
        userId (str): The user's ID
        recipeId (str): The recipe's ID

    Returns:
        JSON response indicating the success of saving the recipe
    Raises:
        400 error if input validation fails.
        500 error if there is an issue adding the song to the playlist.
    """
    app.logger.info('Saving a recipe to the user profile')
    try:
        data = request.get_json()

        recipe_id = data.get('recipeId')

        app.logger.info('Saving recipe: %s', recipe_id)
        recipe_model.save(recipeId=recipe_id)
        app.logger.info("Recipe saved: %s", recipe_id)
        return make_response(jsonify({'status': 'success', 'receipe': recipe_id}), 201)

    except Exception as e:
        app.logger.error("Failed to add recipe: %s", str(e))
        return make_response(jsonify({'error': str(e)}), 500)


@app.route('/api/preferences', methods=['PUT'])
def preferences() -> Response:
    """
    Updates the users recipe preferences

    Returns:
        JSON response with user recipe preferences
    """
    app.logger.info("Updating user preferences")
    try:
        data = request.get_json()

        # Need to add converting preferences string into tuple of (ingredient, calorie, diet)
        preferences = data.get('preferences')



        app.logger.info('Updating preferences')
        recipe_account_model.update_preferences(preferences=preferences)

        app.logger.info("Preferences updated")
        return make_response(jsonify({'status': 'success', 'preferences': preferences}), 200)

    except Exception as e:
        app.logger.error("Failed to update preferences: %s", str(e))
        return make_response(jsonify({'error': str(e)}), 500)

@app.route('/api/get-preferences', methods=['GET'])
def getPreferences() -> Response:
    """
    Gets the users recipe preferences

    Returns:
        JSON response indicating the retrieval of the preferences of failure
    """
    app.logger.info("Retrieving user preferences")
    try:
        data = request.get_json()

        preferences = data.get('preferences')
        
        app.logger.info('Retrieving preferences')
        recipe_account_model.get_user_preferences()

        app.logger.info("Preferences retrieved")
        return make_response(jsonify({'status': 'success', 'preferences': preferences}), 200)

    except Exception as e:
        app.logger.error("Failed to update preferences: %s", str(e))
        return make_response(jsonify({'error': str(e)}), 500)
