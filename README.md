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

### **1. `/search`**

- **Path**: `/api/search`

- **Request Type**: `GET`

- **Purpose**: Search for recipes based on ingredients and optional filters like dietary restrictions and calorie limits.

- **Request Format**:

  - **GET Parameters**:

    - `ingredients` (string, required): Comma-separated list of ingredients (e.g., `chicken,tomato`).

    - `diet` (string, optional): Dietary restriction (e.g., `vegan`, `keto`).

    - `calories` (string, optional): Calorie range (e.g., `200-400`).

- **Response Format**:

  {

    "status": "success",

    "recipes": [

      {

        "title": "Grilled Chicken Salad",

        "ingredients": ["chicken", "lettuce", "tomato"],

        "calories": 350,

        "instructions": "Mix ingredients and grill chicken."

      }

    ]

  }

  ```

- **Example**:

  curl -X GET "http://localhost:5000/api/search?ingredients=chicken,tomato&diet=keto&calories=200-400"

---

### **2. `/recommend`**

- **Path**: `/api/recommend`

- **Request Type**: `GET`

- **Purpose**: Provide personalized recipe recommendations based on user preferences and optional cuisine type.

- **Request Format**:

  - **GET Parameters**:

    - `userId` (string, required): Unique ID of the user.

    - `cuisine` (string, optional): Preferred cuisine type (e.g., `Indian`, `Italian`).

- **Response Format**:

  {

    "status": "success",

    "recipes": [

      {

        "title": "Chicken Biryani",

        "cuisine": "Indian",

        "calories": 450,

        "ingredients": ["chicken", "rice", "spices"]

      }

    ]

  }

  ```

- **Example**:

  curl -X GET "http://localhost:5000/api/recommend?userId=123&cuisine=Indian"

---

### **3. `/trending`**

- **Path**: `/api/trending`

- **Request Type**: `GET`

- **Purpose**: Display trending recipes based on popularity.

- **Request Format**:

  - No parameters required.

- **Response Format**:

  {

    "status": "success",

    "recipes": [

      {

        "title": "Avocado Toast",

        "popularity": 95,

        "ingredients": ["avocado", "bread"]

      }

    ]

  }

- **Example**:

  curl -X GET "http://localhost:5000/api/trending"

---

### **4. `/save`**

- **Path**: `/api/save`

- **Request Type**: `POST`

- **Purpose**: Save a recipe to the user's profile for future access.

- **Request Format**:

  - **POST Body**:

    {

      "userId": "123",

      "recipeId": "456"

    }

    ```

- **Response Format**:

  {

    "status": "success",

    "message": "Recipe saved successfully."

  }

  ```

- **Example**:

  curl -X POST "http://localhost:5000/api/save"

  -H "Content-Type: application/json"

  -d '{

        "userId": "123",

        "recipeId": "456"

      }'

  ```

---

### **5. `/preferences`**

- **Path**: `/api/preferences`

- **Request Type**: `PUT`

- **Purpose**: Update user dietary preferences, including favorite cuisines and calorie limits.

- **Request Format**:

  - **PUT Body**:

    {

      "userId": "123",

      "preferences": {

        "diet": "vegan",

        "calories": "1500"

      }

    }

    ```

- **Response Format**:

  {

    "status": "success",

    "message": "Preferences updated successfully."

  }

  ```

- **Example**:

  curl -X PUT "http://localhost:5000/api/preferences"

  -H "Content-Type: application/json"

  -d '{

        "userId": "123",

        "preferences": {

          "diet": "vegan",

          "calories": "1500"

        }

      }'

  ```

---

### **6. `/get-preferences`**

- **Path**: `/api/get-preferences`

- **Request Type**: `GET`

- **Purpose**: Retrieve user dietary preferences.

- **Request Format**:

  - **GET Parameters**:

    - `userId` (string, required): Unique ID of the user.

- **Response Format**:

  {

    "status": "success",

    "preferences": {

      "diet": "vegan",

      "calories": "1500",

      "favoriteCuisines": ["Indian", "Mexican"]

    }

  }

  ```

- **Example**:

  curl -X GET "http://localhost:5000/api/get-preferences?userId=123"
