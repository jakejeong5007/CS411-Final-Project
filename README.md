Recipe Finder

Overview

Recipe Finder is a web application designed to simplify the process of discovering, saving, and managing recipes. It is built with a focus on personalization and accessibility, allowing users to search for recipes based on the ingredients they have at hand, explore trending recipes, and receive tailored recommendations based on their dietary preferences and favorite cuisines.

The application integrates with external APIs like the Spoonacular API or Edamam Recipe API to fetch comprehensive recipe data, including nutritional details, preparation steps, and ingredient lists. By combining a user-friendly interface with powerful search and recommendation features, Recipe Finder transforms the way users plan meals and explore new dishes.

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

    **Preferences Object Structure**:

    | Key | Type | Description |
    | --- | --- | --- |
    | `diet` | string | Dietary preference (e.g., `vegan`). |
    | `calories` | string | Daily calorie limit (e.g., `1500`). |
    | `ingredient` | String | Ingredient preference (e.g., 'rice'). |

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

-   **Preferences Object Structure**:

    | Key | Type | Description |
    | --- | --- | --- |
    | `diet` | string | Dietary preference (e.g., `vegan`). |
    | `calories` | string | Daily calorie limit (e.g., `1500`). |
    | `ingredient` | String | Ingredient preference (e.g., 'rice'). |

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
