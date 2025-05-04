from flask import Flask, request, jsonify
from utils.ingredients import load_ingredients_from_csv
from utils.recipes import generate_meal_plan

app = Flask(__name__)

@app.route('/generate-meal-plan', methods=['POST'])
def meal_plan():
    data = request.get_json()
    liked_dishes = data.get("liked_dishes")
    if not liked_dishes:
        return jsonify({"error": "No liked dishes provided"}), 400
    
    pantry = load_ingredients_from_csv("receipt_items.csv")
    plan, shopping_list = generate_meal_plan(liked_dishes, pantry)

    return jsonify({
        "meal_plan": plan,
        "shopping_list": shopping_list
    })

if __name__ == '__main__':
    app.run(debug=True)
                            
