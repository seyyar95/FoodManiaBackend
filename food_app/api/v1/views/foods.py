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
    # Get the data from the request
    data = request.get_json()
    ingredient = data.get('ingredients')
    
    # Return an error if the ingredient is not provided
    if not ingredient:
        return jsonify({'error': 'Ingredient is required'}), 400
    
    # Get the foods that contain the ingredient
    foods = Food.get_foods_by_ingredients(ingredient)

    foods_list = []

    # Create a dictionary with the food data
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
    # Get the data from the request
    data = request.get_json()

    # Get the food by name
    food = storage.get_by_name(Food, data.get('name'))
    
    # Create a dictionary with the food data if the food is found
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
    # Get the data from the request
    data = request.get_json()
    food_id = data.get('id')

    # Return an error if the food id is not provided
    if not food_id:
        return jsonify({'error': 'Food id is required'}), 400
    
    # Get the food by id
    food = storage.get_by_id(Food, food_id)

    # Return an error if the food is not found
    if not food:
        return jsonify({'error': 'Food not found'}), 404


    # Create a dictionary with the food data
    food_dict = { 
        'steps': food.steps.split('.'),
        'ingredients': []
    }

    # Get the ingredients for the food
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
    # Get the user id from the JWT
    userjwt_id = get_jwt_identity()

    # Get the data from the request
    data = request.get_json()
    food_id = data.get('food_id')

    # Get food and user objects by id
    food = storage.get_by_id(Food, food_id)
    user = storage.get_by_id(User, userjwt_id)

    # Create a new FoodSave object and save it to the database if the user and the food exists
    if (request.method == 'POST' and user and food):
        save = FoodSave(user_id = userjwt_id, food_id = food_id)
        session = storage.get_session()
        save_second = session.query(FoodSave).filter(FoodSave.user_id == userjwt_id, FoodSave.food_id == food_id).first()
        if(save_second):
            return "save olunub"
        save.save()
        return " ", 201
    
    # Delete the FoodSave object from the database if the user exists
    if (request.method == 'PATCH' and user and food):
        session = storage.get_session()
        save_delete = session.query(FoodSave).filter(FoodSave.user_id == userjwt_id, FoodSave.food_id == food_id).first().delete()
        return " ", 200
    return " ",  403