"""
File that handles functions like 

save -> Saves recipe to user's profie
preferences -> sets selected recipes to prefered recipe for specific user
get_preferences -> gets current preference
"""

def saveRecipe(user_id, recipe_id):
  data = {
    "userId": user_id,
    "recipeId": recipe_id
  }
  response = requests.post("/save", json = data)
  if response.status_code == 200:
    
