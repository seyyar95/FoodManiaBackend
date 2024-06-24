from api.v1.views import app_views
from flask import jsonify, request, current_app, url_for, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.daily_suggest import DailySuggestion
from models.users import User
from models.foods import Food
from models.ingredients import Ingredient
from models.food_ingredient import FoodIngredient
from models.foodsave import FoodSave
from models import storage
import os
import random


@app_views.route('/search_foods_by_ingredient',  methods=['GET'], strict_slashes=False)
@jwt_required()
def get_foods_by_ingredient():
    # Get the data from the request
    data = request.get_json()
    ingredient = data.get('ingredients')

    # get the user id from the JWT
    user_id = get_jwt_identity()
    
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
            'img': food.img,
            'saved': any(saved.user_id == user_id for saved in food.foodsave)
        }
        
        foods_list.append(food_dict)

    return jsonify(foods_list), 200


@app_views.route('/search_foods_by_name',  methods=['GET'], strict_slashes=False)
@jwt_required()
def get_food_by_names():
    # Get the data from the request
    data = request.get_json()
    search_name = data.get('name')

    # Get the user id from the JWT
    user_id = get_jwt_identity()


    if not search_name:
        return jsonify({'error': 'Name parameter is required'}), 400

    all_foods = storage.all(Food)

    # Filter foods that contain the search name
    foods_to_get = [food for food in all_foods.values() if search_name in food.name]

    foods_to_show = []
    # Create a dictionary with the food data if the food is found
    for food in foods_to_get:
        food_dict = {
           'name': food.name,
           'id': food.id,
           'img': food.img,
           'saved': any(saved.user_id == user_id for saved in food.foodsave)
        }

        foods_to_show.append(food_dict)
    
    return jsonify(foods_to_show), 200




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
        'description': food.description,
        'time': food.time,
        'degree': food.degree,
        'steps': food.steps.split('|'),
        'ingredients': []
    }

    # Get the ingredients for the food
    for food_ingredient in food.ingredients:
        ingredient = storage.get_by_id(Ingredient, food_ingredient.ingredient_id)
        if ingredient:
            food_dict['ingredients'].append({
                'name': ingredient.name,
                'img': ingredient.img,
                'quantity': food_ingredient.quantity
            })

    return jsonify(food_dict), 200


@app_views.route('/save', methods=['GET', 'POST'], strict_slashes=False)
@jwt_required()
def save_food():
    # Get the user id from the JWT
    user_id = get_jwt_identity()

    session = storage.get_session()
    user = storage.get_by_id(User, user_id)
    
    # Create a new FoodSave object and save it to the database if the user and the food exists
    if request.method == 'POST' and user:
        data = request.get_json()
        food_id = data.get('food_id')

        food = storage.get_by_id(Food, food_id)

        already_saved = session.query(FoodSave).filter(FoodSave.user_id == user.id, FoodSave.food_id == food.id).first()

        if already_saved:
            session.query(FoodSave).filter(FoodSave.user_id == user.id, FoodSave.food_id == food_id).first().delete()

            return jsonify({
            "id": food_id
            }), 200

        save_food = FoodSave(user_id = user_id, food_id = food_id)
        save_food.save()

        return jsonify({
            "id": food_id
        }), 201
    
    # Get all saved foods for the user
    if request.method == 'GET' and user:
        session = storage.get_session()

        # Query the database for the foods saved by the user
        foods = session.query(Food).join(FoodSave).filter(FoodSave.user_id == user.id).all()

        foods_list = []

        # Create a dictionary with the food data
        for food in foods:
            
            food_dict = {
                'name': food.name,
                'id': food.id,
                'img': food.img,
                'saved': True
            }

            foods_list.append(food_dict)

        # Return the list of saved foods    
        return jsonify(foods_list), 200


@app_views.route('/daily_suggestion', methods=['GET'], strict_slashes=False)
@jwt_required()
def daily_suggestion():
    user_id = get_jwt_identity()
    daily_foods_id  = list(storage.all(DailySuggestion).values())
    food_list = []
    for food in daily_foods_id:
        foods = storage.get_by_id(Food ,food.food_id)
        if foods:
            food_dict = {
                'name': foods.name,
                'id': foods.id,
                'img': foods.img,
                'saved': any(saved.user_id == user_id for saved in foods.foodsave)
            }
            food_list.append(food_dict)
    return jsonify(food_list), 200




@app_views.route('/add_data', methods=['POST'], strict_slashes=False)
def add_data():
    datas = request.get_json()
    for data in datas:
        name = data.get('name')
        description = data.get('description')
        steps = data.get('steps')
        time = data.get('time')
        degree = data.get('degree')
        img = data.get('img')
        ingredients = data.get('ingredients')

        already_added = storage.get_by_name(Food, name)
        if not already_added:
            food = Food(name=name, steps=steps, description=description, time=time, degree=degree, img=img)
            food.save()

            for ing in ingredients:
                existing_ing = storage.get_by_name(Ingredient, ing.get('name'))
                if existing_ing:
                    foodingredient = FoodIngredient(food=food, ingredient=existing_ing, quantity=ing.get('quantity'))   
                else:
                    ingredient = Ingredient(name=ing.get('name'), img=ing.get('img'))
                    ingredient.save()
                    foodingredient = FoodIngredient(food=food, ingredient=ingredient, quantity=ing.get('quantity'))
                foodingredient.save()

