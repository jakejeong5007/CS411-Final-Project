"""
File that handles functions like 

save -> Saves recipe to user's profie
preferences -> sets selected recipes to prefered recipe for specific user
get_preferences -> gets current preference
"""

class RecipeAccountModel:
  """
    A class to manage the functionalities of a user's account
  """
  
  def save_recipe(user_id, recipe_id):
    """ Save a recipe to a user's account
    """
    logger.info('Saving new preferences for user %s', user_id)
    
    if not isinstance(preferences, dict):
      logger.error("Preferences must be a valid dictionary")
      raise TypeError("Preferences must be a valid dictionary")

    if not user_id:
      logger.error("User ID is invalid or missing")
      raise ValueError("User ID must be provided")

    existing_preferences = self.preferences_dict.get(user_id)
    if existing_preferences == preferences:
      logger.warning("Preferences for User ID %s are already up to date", user_id)
      return

    self.preferences_dict[user_id] = preferences
        logger.info("Preferences successfully saved for User ID %s", user_id)

  def update_preferences(user_id, preferences):
    """ Update user preferneces
    """
    logger.info("Adding recipe %s to preferences for user %s", recipe_id, user_id)

    if not user_id or not recipe_id:
      logger.error("User ID and Recipe ID must be provided")
      raise ValueError("User ID and Recipe ID must be provided")

    if user_id not in self.preferences_dict:
      self.preferences_dict[user_id] = {"recipes": []}


    user_recipes = self.preferences_dict[user_id].get("recipes", [])
    if recipe_id in user_recipes:
      logger.warning("Recipe %s is already saved for User ID %s", recipe_id, user_id)
      return

    user_recipes.append(recipe_id)
    self.preferences[user_id]["recipes"] = user_recipes
    logger.info("Recipe %s added successfully for User ID %s", recipe_id, user_id)

  def get_preferences(user_id, preferences):
    """ Retrieve user preferences
    """
    logger.info("Fetching preferences for user %s", user_id)

    if not user_id:
      logger.error("User ID is invalid or missing")
      raise ValueError("User ID must be provided")

    return self.preferences.get(user_id, {})
    

    
    
