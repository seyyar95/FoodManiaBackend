from api.v1.views import app_views
from flask import jsonify, request
from models.foods import Food
from models.ingredients import Ingredient
from flask_jwt_extended import jwt_required
from models.food_ingredient import FoodIngredient


@app_views.route('/search_foods_by_ingridient',  methods=['GET'], strict_slashes=False)
# @jwt_required()
def get_foods_by_ingredient():
    # data = request.get_json()
    # ingredient = data.get('ingredient')
    # if not ingredient:
    #     return jsonify({'error': 'Ingredient is required'}), 400
    ingredients = ['Pasta', 'Lettuce', 'Tomatoes'] 
    
    ingredients_ = Ingredient.get_ingredients_ids(ingredients)
    ingredient_ids = []
    for ingredient in ingredients_:
        ingredient_ids.append(ingredient['id'])

      
    
    foods = Food.get_foods_by_ingredients(ingredient_ids)
    


    foods_list = []

    for food, food_ingredient in foods:
        food_dict = {
            'name': food.name,
            'recipe': food.recipe,
            'ingredients': []
        }
     

        print(food_ingredient.ingredient_id)
        for ingredients in food.ingredients:            
            food_dict['ingredients'].append({
                'quantity': ingredients.quantity
             })

        # for ing in food_ingredient:
        #     print(ing.id)
        #     print(ing.quantity)
        
        


        foods_list.append(food_dict)
    
    return jsonify(foods_list)