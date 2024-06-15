from api.v1.views import app_views
from flask import jsonify, request, current_app, url_for, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.users import User
from models.foods import Food
from models.ingredients import Ingredient
from models.food_ingredient import FoodIngredient
from models.foodsave import FoodSave
from models import storage
import os



@app_views.route('/images/<filename>', methods=['GET'], strict_slashes=False)
def get_image(filename):
    # Construct the full path to the image
    image_path = os.path.join(current_app.config['FOODS_PICTURES'], filename)
    
    if not os.path.exists(image_path):
        return jsonify({'error': 'Image not found'}), 404

    return send_file(image_path)



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
        food_pic = url_for('app_views.get_image', filename='download.jpg', _external=True)
        
        food_dict = {
            'name': food.name,
            'id': food.id,
            'img': food_pic
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
    search_name = data.get('name')

    if not search_name:
        return jsonify({'error': 'Name parameter is required'}), 400

    all_foods = storage.all(Food)

    # Filter foods that contain the search name
    foods_to_get = [food for food in all_foods.values() if search_name in food.name]

    food_pic = url_for('app_views.get_image', filename='download.jpg', _external=True)
    
    foods_to_show = []
    # Create a dictionary with the food data if the food is found
    for food in foods_to_get:
        food_dict = {
            'name': food.name,
            'id': food.id,
            'img': food_pic
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
        'steps': food.steps.split('|'),
        'ingredients': []
    }

    # Get the ingredients for the food
    for food_ingredient in food.ingredients:
        ingredient = storage.get_by_id(Ingredient, food_ingredient.ingredient_id)
        if ingredient:
            
            ingredient_pic = url_for('app_views.get_image', filename='download.jpg', _external=True)

            food_dict['ingredients'].append({
                'name': ingredient.name,
                'img': ingredient_pic
                'quantity': food_ingredient.quantity
            })

    return jsonify(food_dict), 200


@app_views.route('/save', methods=['GET', 'POST', 'PATCH'], strict_slashes=False)
@jwt_required()
def save_food():
    # Get the user id from the JWT
    userjwt_id = get_jwt_identity()

    # Get the data from the request
    data = request.get_json()
    food_id = data.get('food_id')

    # Get food object by id
    food = storage.get_by_id(Food, food_id)

    # Return an error if the food is not found
    if not food:
        return jsonify({'error': 'Food not found'}), 404
    
    # Get user object by id
    user = storage.get_by_id(User, userjwt_id)

    # Return an error if the user is not found
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Create a new FoodSave object and save it to the database if the user and the food exists
    if (request.method == 'POST' and user and food):
        save = FoodSave(user_id = userjwt_id, food_id = food_id)
        session = storage.get_session()
        save_second = session.query(FoodSave).filter(FoodSave.user_id == user.id, FoodSave.food_id == food.id).first()
        if(save_second):
            return "save olunub"
        save.save()
        return " ", 201
    
    # Unsave the food if the user and the food exists
    if (request.method == 'PATCH' and user and food):
        session = storage.get_session()
        save_delete = session.query(FoodSave).filter(FoodSave.user_id == user.id, FoodSave.food_id == food_id).first().delete()
        return " ", 200
    
    # Get all saved foods for the user
    if (request.method == 'GET' and user):
        session = storage.get_session()
        foods = session.query(Food).join(FoodSave).filter(FoodSave.user_id == user.id).all()
        foods_list = []
        for food in foods:
            food_pic = url_for('app_views.get_image', filename='download.jpg', _external=True)
            food_dict = {
                'name': food.name,
                'id': food.id,
                'img': food_pic
            }
            foods_list.append(food_dict)
        return jsonify(foods_list), 200

    return " ",  403