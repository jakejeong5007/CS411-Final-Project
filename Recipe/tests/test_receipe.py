import pytest
from unittest.mock import patch
from flask import Flask

from app import app

######################################################
#
#    Fixtures
#
######################################################

@pytest.fixture
def client():
    """Fixture to provide a test client for the Flask app."""
    app.testing = True
    with app.test_client() as client:
        yield client


######################################################
#
#    Tests for /search API
#
######################################################

@patch('recipe_model.search_recipes')
def test_search_success(mock_search_recipes, client):
    """Test searching for recipes successfully."""
    mock_search_recipes.return_value = [
        {"title": "Test Recipe", "calories": 250, "ingredients": ["chicken", "tomato"]}
    ]

    response = client.get('/api/search?ingredients=chicken,tomato&diet=vegan&calories=200-400')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == "success"
    assert len(data['recipes']) == 1
    assert data['recipes'][0]['title'] == "Test Recipe"

def test_search_missing_ingredients(client):
    """Test searching for recipes with missing ingredients parameter."""
    response = client.get('/api/search?diet=vegan')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_search_invalid_calories(client):
    """Test searching for recipes with an invalid calorie range."""
    response = client.get('/api/search?ingredients=chicken,tomato&calories=not-a-range')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


######################################################
#
#    Tests for /recommend API
#
######################################################

@patch('recipe_account_model.get_user_preferences')
@patch('recipe_model.recommend_recipes')
def test_recommend_success(mock_recommend_recipes, mock_get_user_preferences, client):
    """Test successful recipe recommendations."""
    mock_get_user_preferences.return_value = {"diet": "vegan", "calories": 1500}
    mock_recommend_recipes.return_value = [
        {"title": "Recommended Recipe", "calories": 350, "cuisine": "Italian"}
    ]

    response = client.get('/api/recommend?userId=user123&cuisine=Italian')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == "success"
    assert len(data['recipes']) == 1
    assert data['recipes'][0]['title'] == "Recommended Recipe"

def test_recommend_missing_user_id(client):
    """Test recommending recipes without userId parameter."""
    response = client.get('/api/recommend?cuisine=Italian')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

@patch('recipe_account_model.get_user_preferences')
def test_recommend_no_preferences(mock_get_user_preferences, client):
    """Test recommending recipes for a user without preferences."""
    mock_get_user_preferences.return_value = None
    response = client.get('/api/recommend?userId=user123&cuisine=Italian')
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data


######################################################
#
#    Tests for /trending API
#
######################################################

@patch('recipe_model.get_trending_recipes')
def test_trending_success(mock_get_trending_recipes, client):
    """Test fetching trending recipes successfully."""
    mock_get_trending_recipes.return_value = [
        {"title": "Trending Recipe", "popularity": 95}
    ]

    response = client.get('/api/trending')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == "success"
    assert len(data['recipes']) == 1
    assert data['recipes'][0]['title'] == "Trending Recipe"

@patch('recipe_model.get_trending_recipes')
def test_trending_no_results(mock_get_trending_recipes, client):
    """Test fetching trending recipes when there are no results."""
    mock_get_trending_recipes.return_value = []

    response = client.get('/api/trending')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == "success"
    assert len(data['recipes']) == 0


######################################################
#
#    Tests for /save API
#
######################################################

@patch('recipe_account_model.save_recipe')
def test_save_recipe_success(mock_save_recipe, client):
    """Test saving a recipe successfully."""
    response = client.post('/api/saveRecipe', json={"userId": "user123", "recipeId": "recipe456"})
    assert response.status_code == 201
    data = response.get_json()
    assert data['status'] == "success"

def test_save_recipe_missing_fields(client):
    """Test saving a recipe with missing required fields."""
    response = client.post('/api/saveRecipe', json={"userId": "user123"})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


######################################################
#
#    Tests for /preferences API
#
######################################################

@patch('recipe_account_model.update_preferences')
def test_preferences_update_success(mock_update_preferences, client):
    """Test updating user preferences successfully."""
    response = client.put('/api/preferences', json={
        "userId": "user123",
        "preferences": {"diet": "vegan", "calories": 1500}
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == "success"

def test_preferences_update_missing_fields(client):
    """Test updating preferences with missing required fields."""
    response = client.put('/api/preferences', json={"userId": "user123"})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


######################################################
#
#    Tests for /get-preferences API
#
######################################################

@patch('recipe_account_model.get_preferences')
def test_get_preferences_success(mock_get_preferences, client):
    """Test fetching user preferences successfully."""
    mock_get_preferences.return_value = {"diet": "keto", "calories": 2000}
    response = client.get('/api/get-preferences?userId=user123')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == "success"
    assert data['preferences']['diet'] == "keto"

def test_get_preferences_missing_user_id(client):
    """Test fetching preferences without userId parameter."""
    response = client.get('/api/get-preferences')
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data