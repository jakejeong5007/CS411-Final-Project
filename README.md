Recipe Finder

Overview

Recipe Finder is a web application designed to simplify the process of discovering, saving, and managing recipes. It is built with a focus on personalization and accessibility, allowing users to search for recipes based on the ingredients they have at hand, explore trending recipes, and receive tailored recommendations based on their dietary preferences and favorite cuisines.

The application integrates with external APIs like the Spoonacular API or Edamam Recipe API to fetch comprehensive recipe data, including nutritional details, preparation steps, and ingredient lists. By combining a user-friendly interface with powerful search and recommendation features, Recipe Finder transforms the way users plan meals and explore new dishes.

**Note: For the external API, you need to pay for it. Therefore, we have the code for the case you have the API key commented out. For now, the API call returns an dummy value of an empty list (Should return a list of recipies when having a API key)**

Key Features:

1\. **Ingredient-Based Search**: Users can input a list of available ingredients to find recipes that match, making it easy to use up ingredients in their kitchen.

2\. **Personalized Recommendations**: Recipes are suggested based on user-specific preferences such as favorite ingredients, calorie ranges, or dietary restrictions.

3\. **Trending Recipes**: Users can explore recipes that are popular and trending among the community.

4\. **Profile Management**: Save favorite recipes, set dietary preferences, and update preferences at any time.

5\. **Calorie and Dietary Filters**: Search for recipes that fit specific calorie ranges or dietary needs such as vegan, keto, or gluten-free.

---

## API Documentation

### 1\. `/search`

-   **Route Name**: Search Recipes
-   **Path**: `/api/search`
-   **Request Type**: `GET`
-   **Purpose**: Search for recipes based on a list of ingredients and optional filters such as dietary restrictions and calorie limits.

#### Request Format
-   **Request Body**:

    | Parameter | Type | Required | Description |
    | --- | --- | --- | --- |
    | `ingredients` | string | Yes | Comma-separated list of ingredients (e.g., `chicken,tomato`). |
    | `diet` | string | No | Dietary restriction (e.g., `vegan`, `keto`). |
    | `calories` | int | No | Calorie (e.g., 200). |

#### Response Format

-   **JSON Keys and Value Types**:

    | Key | Type | Description |
    | --- | --- | --- |
    | `status` | string | Status of the response (e.g., `success`). |

#### Example
-  **Success Response Example:**
    - Code: 200
    - Content: { "recipes": [Recipe] }
      

**Request via JSON**:

*Note: Although `GET` requests typically use URL parameters, some tools allow sending a JSON body.*

```
{
  "ingredients": "chicken,tomato",
  "diet": "keto",
  "calories": 200
}

```

**Associated JSON Response**:

```
{
  "status": "success",
  "recipes": [
    {
      "title": "Grilled Chicken Salad",
      "ingredients": ["chicken", "lettuce", "tomato"],
      "calories": 350
    }
  ]
}

```

* * * * *

### 2\. `/recommend`

-   **Route Name**: Recommend Recipes
-   **Path**: `/api/recommend`
-   **Request Type**: `GET`
-   **Purpose**: Provide personalized recipe recommendations based on user preferences and an optional cuisine type.

#### Request Format

-   **GET Parameters**:

    | Parameter | Type | Required | Description |
    | --- | --- | --- | --- |
    | `cuisine` | string | No | Preferred cuisine type (e.g., `Indian`, `Italian`). |

#### Response Format

-   **JSON Keys and Value Types**:

    | Key | Type | Description |
    | --- | --- | --- |
    | `status` | string | Status of the response (e.g., `success`). |


#### Example
-  **Success Response Example:**
    - Code: 200
    - Content: { "recipes": [Recipe] }

**Request via JSON**:

*Note: Although `GET` requests typically use URL parameters, some tools allow sending a JSON body.*

```
{
  "cuisine": "Indian"
}

```

**Associated JSON Response**:

```
{
  "status": "success",
  "recipes": [
    {
      "title": "Chicken Biryani",
      "calories": 450,
      "ingredients": ["chicken", "rice", "spices"]
    }
  ]
}

```

* * * * *

### 3\. `/trending`

-   **Route Name**: Trending Recipes
-   **Path**: `/api/trending`
-   **Request Type**: `GET`
-   **Purpose**: Display trending recipes based on popularity.

#### Request Format

-   **No parameters required.**

#### Response Format

-   **JSON Keys and Value Types**:

    | Key | Type | Description |
    | --- | --- | --- |
    | `status` | string | Status of the response (e.g., `success`). |


#### Example
-  **Success Response Example:**
    - Code: 200
    - Content: { "recipes": [Recipe] }

**Request via cURL**:


**Request via JSON**:

*No JSON body is required for this `GET` request.*

**Associated JSON Response**:

```
{
  "status": "success",
  "recipes": [
    {
      "title": "Avocado Toast",
      "ingredients": ["avocado", "bread"],
      "calories": 500
    }
  ]
}

```

* * * * *

### 4\. `/save`

-   **Route Name**: Save Recipe
-   **Path**: `/api/save`
-   **Request Type**: `POST`
-   **Purpose**: Save a recipe to the user's profile for future access.

#### Request Format

-   **POST Body**:

    | Key | Type | Description |
    | --- | --- | --- |
    | `recipeId` | string | Unique ID of the recipe to save. |

    ```
    {
      "recipeId": "456"
    }

    ```

#### Response Format

-   **JSON Keys and Value Types**:

    | Key | Type | Description |
    | --- | --- | --- |
    | `status` | string | Status of the response (e.g., `success`). |

-   **Response Body in Grid Format**:

    | status | message |
    | --- | --- |
    | success | Recipe saved successfully. |

#### Example
-  **Success Response Example:**
    - Code: 201
    - Content: { "recipe": 348 }



**Request via JSON**:

```
{
  "recipeId": "456"
}

```

**Associated JSON Response**:

```
{
  "status": "success",
  "recipe": 348
}

```

* * * * *

### 5\. `/preferences`

-   **Route Name**: Update Preferences
-   **Path**: `/api/preferences`
-   **Request Type**: `PUT`
-   **Purpose**: Update user dietary preferences, including favorite cuisines and calorie limits.

#### Request Format

-   **PUT Body**:

    | Key | Type | Description |
    | --- | --- | --- |
    | `preferences` | object | Object containing user preferences. |


    ```
    {
      "preferences": {
        "diet": "vegan",
        "calories": "1500",
        "preferences": "rice"
      }
    }

    ```

#### Response Format

-   **JSON Keys and Value Types**:

    | Key | Type | Description |
    | --- | --- | --- |
    | `status` | string | Status of the response (e.g., `success`). |

-   **Response Body in Grid Format**:

    | status | message |
    | --- | --- |
    | success | Preferences updated successfully. |

#### Example

**Request via JSON**:

```
{
  "preferences": {
    "diet": "vegan",
    "calories": "1500",
    "preferences": "rice"
  }
}

```


**Associated JSON Response**:

```
{
  "status": "success",
  "preferences": 'vegan', '1500', 'rice'
}

```

* * * * *

### 6\. `/get-preferences`

-   **Route Name**: Get Preferences
-   **Path**: `/api/get-preferences`
-   **Request Type**: `GET`
-   **Purpose**: Retrieve user dietary preferences.

#### Request Format

*No JSON body is required for this `GET` request.*

#### Response Format

-   **JSON Keys and Value Types**:

    | Key | Type | Description |
    | --- | --- | --- |
    | `status` | string | Status of the response (e.g., `success`). |
    | `preferences` | object | Object containing user preferences. |

-   **Response Body in Grid Format**:

    | status | preferences |
    | --- | --- |
    | success | {"diet": "vegan", "calories": "1500", "ingredients": "rice"} |

#### Example

**Request via JSON**:

*No JSON body is required for this `GET` request.*

**Associated JSON Response**:

```
{
  "preferences": {
    "diet": "vegan",
    "calories": "1500",
    "preferences": "rice"
  }
}

```

* * * * *

### 7\. `/login`

- **Route Name**: User Login
- **Path**: `/api/login`
- **Request Type**: `POST`
- **Purpose**: Authenticate a user with a username and password.

#### Request Format
- **Request Body**:

    | Parameter       | Type   | Required | Description                           |
    |-----------------|--------|----------|---------------------------------------|
    | `user_name`     | string | Yes      | The username for the account.         |
    | `user_password` | string | Yes      | The password for the account.         |

#### Response Format

- **JSON Keys and Value Types**:

    | Key             | Type    | Description                                 |
    |-----------------|---------|---------------------------------------------|
    | `status`        | string  | Status of the response (e.g., `success`).   |
    | `user_name`     | string  | The username of the logged-in user.         |
    | `login_status`  | boolean | Whether the login was successful or not.    |

- **Success Response Example**:
    - Code: 201
    - Content:
  ```
  {
    "status": "success",
    "user_name": "example_user",
    "login_status": true
  }
  ```

#### Example

- **Example Request:**
```
{
  "user_name": { "test" },
  "user_password": { "1234" }
}

```

**Associated JSON Response**:

  ```
  {
    "status": "success",
    "user_name": "test",
    "login_status": true
  }
  ```

* * * * *


### 8\. `/create-account`

-   **Route Name**: Create account
-   **Path**: `/api/create-account`
-   **Request Type**: `POST`
-   **Purpose**: Creates a new account with given user name and password.

#### Request Format
- **Request Body**:

    | Parameter       | Type   | Required | Description                           |
    |-----------------|--------|----------|---------------------------------------|
    | `user_name`     | string | Yes      | The username for the account.         |
    | `user_password` | string | Yes      | The password for the account.         |


#### Response Format

- **JSON Keys and Value Types**:

    | Key             | Type    | Description                                 |
    |-----------------|---------|---------------------------------------------|
    | `status`        | string  | Status of the response (e.g., `success`).   |
    | `user_name`     | string  | The username of the logged-in user.         |

#### Example

- **Success Response Example**:
    - Code: 201
    - Content:
  ```
  {
    "status": "success",
    "user_name": "example_user",
    "login_status": true
  }
  ```

#### Example

- **Example Request:**
```
{
  "user_name": { "test" },
  "user_password": { "1234" }
}

```

**Associated JSON Response**:

  ```
  {
    "status": "success",
    "user_name": "test",
  }
  ```

* * * * *

### 9\. `/update-password`

-   **Route Name**: Update password
-   **Path**: `/api/update-password`
-   **Request Type**: `PATCH`
-   **Purpose**: Updates user password.

#### Request Format
- **Request Body**:

    | Parameter       | Type   | Required | Description                           |
    |-----------------|--------|----------|---------------------------------------|
    | `user_name`     | string | Yes      | The username for the account.         |
    | `current_user_password` | string | Yes      | The current password for the account.         |
    | `new_user_password` | string | Yes      | The new password for the account.         |


#### Response Format

- **JSON Keys and Value Types**:

    | Key             | Type    | Description                                 |
    |-----------------|---------|---------------------------------------------|
    | `status`        | string  | Status of the response (e.g., `success`).   |
    | `user_name`     | string  | The username of the logged-in user.         |

#### Example

- **Success Response Example**:
    - Code: 201
    - Content:
  ```
  {
    "status": "success",
    "user_name": "example_user",
    "login_status": true
  }
  ```

#### Example

- **Example Request:**
```
{
  "user_name": { "test" },
  "current_user_password": { "1234" },
  "new_user_password": { "4321" }
}

```

**Associated JSON Response**:

  ```
  {
    "status": "success",
    "user_name": "test",
  }
  ```

* * * * *


