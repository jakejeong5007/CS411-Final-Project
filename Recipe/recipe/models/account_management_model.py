import logging
import os
import sqlite3
import hashlib

from recipe.utils.logger import configure_logger
from recipe.utils.sql_utils import get_db_connection


logger = logging.getLogger(__name__)
configure_logger(logger)
    
salt = os.urandom(16)

def login(user_name: str, user_password: str) -> bool:
    """
    Login with given user name and password
    
    Args:
        user_name (str): The user name
        password (str): The password
    
    Returns:
        success (bool): True if the password matches the given user name. Else, False.
    
    Raises:
        ValueError: If user_name or password are invalid
        sqlite3.Error: For any other datbase errors
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT hashed_password FROM users WHERE username = ?", (user_name,))
            try:
                hashed_db_password = cursor.fetchone()[0]
                if hashed_db_password == hash_password(user_password):
                    logger.info("Successful login with user name: %s", user_name)
                    return True
                else:
                    logger.info("Password does not match with user name: %s", user_name)
                    return False
                
            except TypeError:
                logger.info("User name with %s not found", user_name)
                raise ValueError(f"User name with {user_name} not found")
            
    except sqlite3.Error as e:
        logger.error("Database error while logging in with user name: %s", user_name)
        raise e    
    
def create_account(user_name: str, user_password: str) -> None:
    """
    Creates a new account in users table.
    
    Args:
        user_name (str): The user name
        user_password (str): The password
        
    Raises:
        ValueError: If user_name or password are invalid
        sqlite3.IntegrityError: If user name already exists in the database
        sqlite3.Error: For any other database errors.
    """
    # Validate the required fields
    if not isinstance(user_name, str):
        raise ValueError(f"Invalid user name provided: {user_name} (must be a string)")
    if not isinstance(user_password, str):
        raise ValueError(f"Invalid user password provided: {user_password} (must be a string)")

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                           INSERT INTO users (username, salt, password)
                           VALUES (?, ?, ?)
                           """, (user_name, salt, hash_password(user_password)))
            conn.commit()
            
            logger.info("Account created successfully: %s", user_name)
    except sqlite3.IntegrityError as e:
        logger.error("Account with user name '%s' already exists", user_name)
        raise ValueError(f"Account with user name '{user_name}' already exists")
    except sqlite3.Error as e:
        logger.error("Database error while creating account: %s", str(e))
        raise sqlite3.Error(f"Database error: {str(e)}")
    
def change_password(user_name: str, current_user_password: str, changed_user_password: str) -> None:
    """
    Change password for the given user name account.
    
    Args:
        user_name (str): The user name
        current_user_password (str): Current password
        changed_user_password (str): Password to change to
        
    Raises:
        ValueError: If user_name or  password are invalid
        sqlite3.Error: For any other datbase errors.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT hashed_password FROM users WHERE username = ?", (user_name,))
            try:
                hashed_db_password = cursor.fetchone()[0]
                if hashed_db_password == hash_password(current_user_password):
                    logger.info("Successful login with user name: %s", user_name)
                    cursor.execute("UPDATE users SET hashed_password = ? WHERE username = ?;", 
                                (hash_password(changed_user_password), user_name))
                else:
                    logger.info("Password does not match with user name: %s", user_name)
                cursor.commit()
            except TypeError:
                logger.info("User name with %s not found", user_name)
                raise ValueError(f"User name with {user_name} not found")
            
    except sqlite3.Error as e:
        logger.error("Database error while updating password: %s", user_name)
        raise e    
    
def hash_password(user_password: str) -> str:
    """
    Hash the given password
    
    Args:
        user_password (str): The password
        
    Returns:
        hashed_password (str): The hashed version of password
    """
    
    # Hash the password combined with the salt
    hashed_password = hashlib.sha256((salt + user_password).encode()).hexdigest()

    # Combine salt and hashed password, separated by a special character
    return f"{salt}${hashed_password}"
