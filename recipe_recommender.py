import pandas as pd
import requests

df = pd.read_csv("receipt_items.csv")

# making a list of ingredients with no duplicates
ingredients = df['item'].str.lower().str.strip().unique().tolist()

print("ingredients from receipt:", ingredients)

API_KEY = "344700c8d7d04b578653c78a2a81984d"

endpoint = "https://api.spoonacular.com/recipes/findByIngredients"

params = {
    "ingredients": ",".join(ingredients),
    "number": 5,
    "ranking": 1,
    "apiKey": API_KEY
}

response = requests.get(endpoint, params=params)

if response.status_code == 200:
    recipes = response.json()
    print("\n Recipe Recommendations Based on What's in Your Pantry:\n")
    for i, recipe in enumerate(recipes, 1):
        title = recipe['title']
        used = [ing['name'] for ing in recipe['usedIngredients']]
        missed = [ing['name'] for ing in recipe['missedIngredients']]
        print(f"{i}. {title}")
        print(f"Uses: {', '.join(used)}")
        print(f"Missing: {', '.join(missed)}")
        print(f"Link: https://spoonacular.com/recipes/{'-'.join(title.lower().split())}-{recipe['id']}")
        print()
else:
    print(f"Failed to fetch recipes. Status code: {response.status_code}")
    