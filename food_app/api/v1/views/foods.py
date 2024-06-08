from api.v1.views import app_views
from flask import jsonify, request
from models.foods import Food
from models.ingredients import Ingredient
from flask_jwt_extended import jwt_required
from models.food_ingredient import FoodIngredient
from models import storage


@app_views.route('/search_foods_by_ingredient',  methods=['GET'], strict_slashes=False)
@jwt_required()
def get_foods_by_ingredient():
    data = request.get_json()
    ingredient = data.get('ingredients')
    if not ingredient:
        return jsonify({'error': 'Ingredient is required'}), 400
    # ingredient = ['Pasta', 'Lettuce', 'Tomato'] 
    
    ingredients_ = Ingredient.get_ingredients_ids(ingredient)
    ingredient_ids = []
    for ingredient in ingredients_:
        ingredient_ids.append(ingredient['id'])

      
    
    foods = Food.get_foods_by_ingredients(ingredient_ids)


    foods_list = []

    for food, food_ingredient in foods:
        food_dict = {
            'name': food.name,
            'id': food.id
        }
        # for food_ingredient in food.ingredients:
        #     ingredient = storage.get(Ingredient, food_ingredient.ingredient_id)
        #     if ingredient:
        #         food_dict['ingredients'].append({
        #             'name': ingredient.name,
        #             'quantity': food_ingredient.quantity
        #         })
        
        foods_list.append(food_dict)

    return jsonify(foods_list), 200

    # food1 = Food(name="Pizza", recipe="Dough, sauce, cheese")
    # food1.save()
    # food2 = Food(name="Pasta", recipe="Noodles, sauce")
    # food2.save()

    # ingredient1 = Ingredient(name="Tomato")
    # ingredient1.save()
    # ingredient2 = Ingredient(name="Cheese")
    # ingredient2.save()
    # ingredient3 = Ingredient(name="Flour")
    # ingredient3.save()

    # food_ingredient1 = FoodIngredient(food=food1, ingredient=ingredient1, quantity=2)
    # food_ingredient1.save()
    # food_ingredient2 = FoodIngredient(food=food1, ingredient=ingredient2, quantity=1)
    # food_ingredient2.save()
    # food_ingredient3 = FoodIngredient(food=food2, ingredient=ingredient3, quantity=3)
    # food_ingredient3.save()


@app_views.route('/search_foods_by_name',  methods=['GET'], strict_slashes=False)
# @jwt_required()
def get_food_by_names():
    food = Food.get_food_by_name('Pizza')
    
    
