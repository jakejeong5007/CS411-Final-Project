#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5001/api"

# Flag to control whether to echo JSON output
ECHO_JSON=false

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done


###############################################
#
# Health checks
#
###############################################

# Function to check the health of the service
check_health() {
  echo "Checking health status..."
  curl -s -X GET "$BASE_URL/health" | grep -q '"status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    exit 1
  fi
}

# Function to check the database connection
check_db() {
  echo "Checking database connection..."
  curl -s -X GET "$BASE_URL/db-check" | grep -q '"database_status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Database connection is healthy."
  else
    echo "Database check failed."
    exit 1
  fi
}

##########################################################
#
# Password Management
#
##########################################################
logging_in() {
  user_name=$1
  user_password=$2

  echo "Logging into user account with user name:$user_name"
  curl -s -X POST "$BASE_URL/login" -H "Content-Type: application/json" \
      -d "{\"user_name\":\"$user_name\", \"user_password\":\"$user_password\"}" | grep -q '"status": "success"'

    if [ $? -eq 0 ]; then
      echo "Login done successfully."
    else
      echo "Failed to login."
      exit 1
    fi
}

creating_account() {
  user_name=$1
  user_password=$2

  echo "Creating a new user account with user name:$user_name"
  curl -s -X POST "$BASE_URL/create-account" -H "Content-Type: application/json" \
      -d "{\"user_name\":\"$user_name\", \"user_password\":\"$user_password\"}" | grep -q '"status": "success"'

    if [ $? -eq 0 ]; then
      echo "Account created successfully."
    else
      echo "Failed to create a new account."
      exit 1
    fi
}

updating_password() {
  user_name=$1
  current_user_password=$2
  new_user_password=$3

  echo "Changing account password with user name:$user_name"
  curl -s -X PATCH "$BASE_URL/update-password" -H "Content-Type: application/json" \
      -d "{\"user_name\":\"$user_name\", \"current_user_password\":\"$current_user_password\", \"new_user_password\":\"$new_user_password\"}" | grep -q '"status": "success"'

    if [ $? -eq 0 ]; then
      echo "User password changed successfully."
    else
      echo "Failed to change user password."
      exit 1
    fi
}
##########################################################
#
# Recipe Management
#
##########################################################

search_for_recipes() {
  ingredient=$1
  diet=$2
  calorie=$3

  echo "Searching recipes with ingredient:$ingredient, diet:$diet, calories:$calorie"
  curl -s -X GET "$BASE_URL/search" -H "Content-Type: application/json" \
      -d "{\"ingredients\":\"$ingredient\", \"diet\":\"$diet\", \"calories\":\"$calorie\"}" | grep -q '"status": "success"'

    if [ $? -eq 0 ]; then
      echo "Search for recipes done successfully."
    else
      echo "Failed to search for recipes."
      exit 1
    fi
}

recommend_recipes() {
  cuisine=$1

  echo "Getting recomendation of recipies with cuisine:$cuisine"
  curl -s -X GET "$BASE_URL/recommend" -H "Content-Type: application/json" \
      -d "{\"cuisine\":\"$cuisine\"}" | grep -q '"status": "success"'

    if [ $? -eq 0 ]; then
      echo "Getting recommendation for recipes done successfully."
    else
      echo "Failed to get recommendation for recipes."
      exit 1
    fi
}

trending_recipes() {
  echo "Getting trending recipes"
  response = $(curl -s -X GET "BASE_URL/get_trending_recipes")
  if echo "$response"|grep -q "status":"success"; then
    echo "Trending recipes retrieved successfully"
    if [ "$ECHO_JSON" = true ]; then
      echo "Recipes JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to retrieve trending recipes."
    exit 1
  fi
}

save_recipes() {
  recipe_id=$1
  echo "Saving recipes to user profile"
  curl -s -X GET "$BASE_URL/saveRecipe" -H "Content-Type: application/json" \
      -d "{\"recipe_id\":\"$recipe_id\"}" | grep -q '"status": "success"'

  if [ $? -eq 0 ]; then
    echo "Saving recipe by id done successfully."
  else
    echo "Failed to save recipes."
    exit 1
  fi
}

update_recipe_preferences() {
  preferences=$1

  echo "Updating user recipe preferences"
  curl -s -X GET "$BASE_URL/saveRecipe" -H "Content-Type: application/json" \
      -d "{\"preferences\":\"$preferences\"}" | grep -q '"status": "success"'

  if [ $? -eq 0 ]; then
    echo "Saving preferences done successfully."
  else
    echo "Failed to save preferences."
    exit 1
  fi
}

get_recipe_preferences() {
  echo "Retrieving user recipe preferences"
  response = $(curl -s -X PUT "BASE_URL/get_preferences")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Preferences retrieved successfully."
  else
    echo "Failed to retrieve recipes."
    exit 1
  fi
}


# Health checks
check_health
check_db

# User management
creating_account "test_user" "password123"
logging_in "test_user" "password123"
updating_password "test_user" "password123" "new_password123"
logging_in "test_user" "new_password123"

# Recipe management
search_for_recipes "tomato" "vegetarian" "200"
recommend_recipes "Italian"
trending_recipes
save_recipes "12345"
update_recipe_preferences '{"cuisine":"Asian","diet":"Vegan"}'
get_recipe_preferences

echo "Smoketest completed successfully!"