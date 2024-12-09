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
#    Tests for Health Checks
#
######################################################

def test_healthcheck(client):
    """Test the health check endpoint."""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == "healthy"

@patch('app.check_database_connection')
@patch('app.check_table_exists')
def test_db_check_success(mock_check_db, mock_check_table, client):
    """Test the database check endpoint when the database is healthy."""
    mock_check_db.return_value = True
    mock_check_table.return_value = True

    response = client.get('/api/db-check')
    assert response.status_code == 200
    data = response.get_json()
    assert data['database_status'] == "healthy"

@patch('app.check_database_connection')
@patch('app.check_table_exists')
def test_db_check_failure(mock_check_db, mock_check_table, client):
    """Test the database check endpoint when the database is unhealthy."""
    mock_check_db.side_effect = Exception("Database connection failed")

    response = client.get('/api/db-check')
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data
    assert data['error'] == "Database connection failed"


######################################################
#
#    Tests for Password Management
#
######################################################

@patch('app.validate_user_credentials')
def test_login_success(mock_validate_user, client):
    """Test logging in with valid credentials."""
    mock_validate_user.return_value = True

    response = client.post('/api/login', json={"user_name": "test_user", "user_password": "password123"})
    assert response.status_code == 201
    data = response.get_json()
    assert data['status'] == "success"
    assert data['user_name'] == "test_user"

def test_login_missing_fields(client):
    """Test logging in with missing required fields."""
    response = client.post('/api/login', json={"user_name": "test_user"})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

@patch('app.validate_user_credentials')
def test_login_invalid_credentials(mock_validate_user, client):
    """Test logging in with invalid credentials."""
    mock_validate_user.return_value = False

    response = client.post('/api/login', json={"user_name": "test_user", "user_password": "wrong_password"})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


@patch('app.create_user_account')
def test_create_account_success(mock_create_account, client):
    """Test creating a new user account successfully."""
    mock_create_account.return_value = True

    response = client.post('/api/create-account', json={"user_name": "test_user", "user_password": "password123"})
    assert response.status_code == 201
    data = response.get_json()
    assert data['status'] == "success"
    assert data['user_name'] == "test_user"

def test_create_account_missing_fields(client):
    """Test creating a new user account with missing fields."""
    response = client.post('/api/create-account', json={"user_name": "test_user"})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

@patch('app.create_user_account')
def test_create_account_failure(mock_create_account, client):
    """Test creating a new user account when the account creation fails."""
    mock_create_account.side_effect = Exception("Account creation failed")

    response = client.post('/api/create-account', json={"user_name": "test_user", "user_password": "password123"})
    assert response.status_code == 500
    data = response.get_json()
    assert "error" in data
    assert data['error'] == "Account creation failed"


@patch('app.update_user_password')
def test_update_password_success(mock_update_password, client):
    """Test updating the user password successfully."""
    mock_update_password.return_value = True

    response = client.patch('/api/update-password', json={"user_name": "test_user", "user_password": "new_password123"})
    assert response.status_code == 201
    data = response.get_json()
    assert data['status'] == "success"
    assert data['user_name'] == "test_user"

def test_update_password_missing_fields(client):
    """Test updating the password with missing fields."""
    response = client.patch('/api/update-password', json={"user_name": "test_user"})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

@patch('app.update_user_password')
def test_update_password_failure(mock_update_password, client):
    """Test updating the password when the operation fails."""
    mock_update_password.side_effect = Exception("Password update failed")

    response = client.patch('/api/update-password', json={"user_name": "test_user", "user_password": "new_password123"})
    assert response.status_code == 500
    data = response.get_json()
    assert "error" in data
    assert data['error'] == "Password update failed"


######################################################
#
#    Run Tests
#
######################################################

if __name__ == "__main__":
    pytest.main()
