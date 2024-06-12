from api.v1.views import app_views
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.users import User
from models.foods import Food
from models.ingredients import Ingredient
from models.food_ingredient import FoodIngredient
from models.foodsave import FoodSave
from models import storage


@app_views.route('/search_foods_by_ingredient',  methods=['GET'], strict_slashes=False)
@jwt_required()
def get_foods_by_ingredient():
    data = request.get_json()
    ingredient = data.get('ingredients')
    if not ingredient:
        return jsonify({'error': 'Ingredient is required'}), 400

    foods = Food.get_foods_by_ingredients(ingredient)

    


    foods_list = []

    for food in foods:
        food_dict = {
            'name': food.name,
            'id': food.id,
            'img': food.img
        }
        
        foods_list.append(food_dict)

    return jsonify(foods_list), 200

    # food1 = Food(name="sdsdsads", steps="Dough, sauce, cheese")
    # food1.save()
    # food2 = Food(name="Pasta", steps="Noodles, sauce")
    # food2.save()
    # food3 = Food(name="Pizza", steps="Dough, sauce, cheese")
    # food3.save()

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
    # food_ingredient4 = FoodIngredient(food=food3, ingredient=ingredient1, quantity=2)
    # food_ingredient4.save()
    # food_ingredient5 = FoodIngredient(food=food3, ingredient=ingredient2, quantity=1)
    # food_ingredient5.save()



@app_views.route('/search_foods_by_name',  methods=['GET'], strict_slashes=False)
@jwt_required()
def get_food_by_names():
    data = request.get_json()
    food = storage.get_by_name(Food, data.get('name'))
    if food:
        food_dict = {
            'name': food.name,
            'id': food.id,
            'img': food.img
        }
        return jsonify(food_dict), 200
    else:
        return jsonify({'error': 'Food not found'}), 404




@app_views.route('/details',  methods=['GET'], strict_slashes=False)
@jwt_required()
def get_food_details():
    data = request.get_json()
    food_id = data.get('id')
    if not food_id:
        return jsonify({'error': 'Food id is required'}), 400
    
    food = storage.get_by_id(Food, 1)

    if not food:
        return jsonify({'error': 'Food not found'}), 404

    food_dict = { 
        'steps': food.steps.split('.'),
        'ingredients': []
    }

    for food_ingredient in food.ingredients:
        ingredient = storage.get_by_id(Ingredient, food_ingredient.ingredient_id)
        if ingredient:
            food_dict['ingredients'].append({
                'name': ingredient.name,
                'quantity': food_ingredient.quantity
            })

    return jsonify([food_dict]), 200


@app_views.route('/save', methods=['POST', 'PATCH'], strict_slashes=False)
@jwt_required()
def save_food():
    userjwt_id = get_jwt_identity()
    data = request.get_json()
    food_id = data.get('food_id')
    if (request.method == 'POST' and storage.get_by_id(User, userjwt_id)):
        save = FoodSave(user_id = userjwt_id, food_id = food_id)
        save.save()
        return " ", 201
    if (request.method == 'PATCH' and storage.get_by_id(User, userjwt_id)):
        session = storage.get_session()
        save_delete = session.query(FoodSave).filter(FoodSave.user_id == userjwt_id, FoodSave.food_id == food_id).first().delete()
        return " ", 200
    return " ",  403