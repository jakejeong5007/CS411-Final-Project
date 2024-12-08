"""
File that handles functions like 

save -> Saves recipe to user's profie
preferences -> sets selected recipes to prefered recipe for specific user
get_preferences -> gets current preference
"""

def saveRecipe(user_name, recipe_id):
  data = {
    "userName": user_name,
    "recipeId": recipe_id
  }
  response = requests.post("/save", json = data)
  if response.status_code == 200:
    
