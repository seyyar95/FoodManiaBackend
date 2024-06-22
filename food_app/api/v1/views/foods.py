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
        food_pic = url_for('app_views.get_image', filename='download.jpg', _external=True)
        
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

    food_pic = url_for('app_views.get_image', filename='download.jpg', _external=True)

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
            
            ingredient_pic = url_for('app_views.get_image', filename='tomato.png', _external=True)

            food_dict['ingredients'].append({
                'name': ingredient.name,
                'img': ingredient_pic,
                'quantity': food_ingredient.quantity
            })

    return jsonify(food_dict), 200


@app_views.route('/save', methods=['GET', 'POST', 'PATCH'], strict_slashes=False)
@jwt_required()
def save_food():
    # Get the user id from the JWT
    userjwt_id = get_jwt_identity()

    session = storage.get_session()
    user = storage.get_by_id(User, userjwt_id)
    
    # Create a new FoodSave object and save it to the database if the user and the food exists
    if (request.method == 'POST' and user):
        data = request.get_json()
        food_id = data.get('food_id')

        food = storage.get_by_id(Food, food_id)

        save_second = session.query(FoodSave).filter(FoodSave.user_id == user.id, FoodSave.food_id == food.id).first()

        if(save_second):
            save_delete = session.query(FoodSave).filter(FoodSave.user_id == user.id, FoodSave.food_id == food_id).first().delete()

            return jsonify({
            "id": food_id
        }), 200

        save = FoodSave(user_id = userjwt_id, food_id = food_id)
        save.save()

        return jsonify({
            "id": food_id
        }), 201
    
    # Get all saved foods for the user
    if (request.method == 'GET' and user):
        session = storage.get_session()

        # Query the database for the foods saved by the user
        foods = session.query(Food).join(FoodSave).filter(FoodSave.user_id == user.id).all()

        foods_list = []

        # Create a dictionary with the food data
        for food in foods:
            food_pic = url_for('app_views.get_image', filename='download.jpg', _external=True)
            
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
def daily_suggestion():
    daily_foods_id  = list(storage.all(DailySuggestion).values())
    food_list = []
    for food in daily_foods_id:
        foods = storage.get_by_id(Food ,food.food_id)
        if foods:
            food_dict = {
                'name': foods.name,
                'id': foods.id,
                'img': foods.img
            }
            food_list.append(food_dict)
    return jsonify(food_list), 200




@app_views.route('/add_data', methods=['GET'], strict_slashes=False)
def add_data():
    food1 = Food(name="Three sister Dolma", steps="Dough |sauce |cheese", description="Dolma are a wide array of stuffed vegetables commonly found in Middle Eastern cuisine, but today we're making the popular 3 Sisters Dolma dish, which consists of eggplants, tomatoes, and peppers stuffed with a seasoned ground beef filling and served in an aromatic tomato sauce. Prepared outside over an open flame, this is the perfect recipe for your next big cookout!", time="1 hour", degree="100", img="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjqAdpVUMKiEMenczu4AuIwvsyYI3AAWKM0BYDkgNVXKK8bPIWmiJv1F3aqZvTvy7QEzxnuaSqCQXW-YRMTc2qqrpN9S1fRTlg3GM1liCkNajI4ZykzGpxbOX0KaDK_pAekFsrrW8O2j7Nx/s400/34258478_1056565737824585_2186393504786153472_n.jpg")
    food1.save()
    food3 = Food(name="Pizza", steps="Dough |sauce |cheese", description="This moderately spicy and super hearty pizza includes spicy salami and fresh tomatoes. This pizza will please even the most demanding gourmet.", time="30 mins", degree="80", img="https://pizza.az/upload/resize_cache/iblock/809/359_355_040cd750bba9870f18aada2478b24840a/80956e09d302a120d49b6fd1071fe5b7.jpg")
    food3.save()

    ingredient2 = Ingredient(name="Cheese")
    ingredient2.save()
    ingredient3 = Ingredient(name="Flour")
    ingredient3.save()
    tomato = Ingredient(name="Tomato")
    tomato.save()

    food_ingredient1 = FoodIngredient(food=food1, ingredient=tomato, quantity=2)
    food_ingredient1.save()
    food_ingredient2 = FoodIngredient(food=food1, ingredient=ingredient2, quantity=1)
    food_ingredient2.save()
    food_ingredient4 = FoodIngredient(food=food3, ingredient=tomato, quantity=2)
    food_ingredient4.save()
    food_ingredient5 = FoodIngredient(food=food3, ingredient=ingredient2, quantity=1)
    food_ingredient5.save()

    # food1 = Food(name="3 sister dolma", steps="Mix ground meat and onions together and brown in a large pan. | Add small amount of butter to prevent burning. | While meat is cooking, bring a large pot of water to a boil with a pinch of salt. | Add eggplant and boil for around 5 minutes, or until soft. | Remove from water and set aside to cool. | Slice tops off of bell peppers and tomatoes and set aside. | Dig out seeds and pulp from tomatoes and green peppers. | Save the insides of the tomatoes for later. | Salt and pepper the insides of the tomatoes and peppers and set aside. | Rub eggplants between hands until soft. | Cut deep slits in eggplants and remove most of the middle. | Salt and pepper the insides of the eggplant. | Add insides of tomatoes and basil to the meat. | Add cinnamon and mix. | Stuff tomatoes, peppers, and eggplants with meat. | Spread green beans out in the pan. | Place stuffed veggies on top and add enough water to cover the bottoms. | Steam over medium heat for 20 minutes or until soft then serve.",)
    # food1.save()
    # food1.img = "3_sister_dolma" + str(food1.id)
    # storage.save()
    # ground_mutton = Ingredient(name="Ground Mutton")
    # ground_mutton.save()
    # onion = Ingredient(name="Onion")
    # onion.save()
    # green_bell_pepper = Ingredient(name="Green Bell Pepper")
    # green_bell_pepper.save()
    # eggplant = Ingredient(name="Eggplant")
    # eggplant.save()
    # green_bean = Ingredient(name="Green Bean")
    # green_bean.save()
    # basil = Ingredient(name="Basil")
    # basil.save()
    # cinnamon = Ingredient(name="Cinnamon")
    # cinnamon.save()
    # butter = Ingredient(name="Butter")
    # butter.save()
    # water = Ingredient(name="Water")
    # water.save()
    # salt = Ingredient(name="Salt")
    # salt.save()
    # black_pepper = Ingredient(name="Black Pepper")
    # black_pepper.save()

    # food_ingredient = FoodIngredient(food=food1, ingredient=ground_mutton, quantity="4 cups")
    # food_ingredient.save()
    # food_ingredient2 = FoodIngredient(food=food1, ingredient=onion, quantity="1 yellow onion")
    # food_ingredient2.save()
    # food_ingredient3 = FoodIngredient(food=food1, ingredient=green_bell_pepper, quantity="6")
    # food_ingredient3.save()
    # food_ingredient4 = FoodIngredient(food=food1, ingredient=eggplant, quantity="6")
    # food_ingredient4.save()
    # food_ingredient5 = FoodIngredient(food=food1, ingredient=green_bean, quantity="1-2 cups")
    # food_ingredient5.save()
    # food_ingredient6 = FoodIngredient(food=food1, ingredient=basil, quantity="3 tablespoons")
    # food_ingredient6.save()
    # food_ingredient7 = FoodIngredient(food=food1, ingredient=cinnamon, quantity="1 teaspoon")
    # food_ingredient7.save()
    # food_ingredient8 = FoodIngredient(food=food1, ingredient=butter, quantity="2 tablespoons")
    # food_ingredient8.save()
    # food_ingredient9 = FoodIngredient(food=food1, ingredient=water, quantity="1/2 cup")
    # food_ingredient9.save()
    # food_ingredient10 = FoodIngredient(food=food1, ingredient=salt, quantity="2 teaspoon")
    # food_ingredient10.save()
    # food_ingredient11 = FoodIngredient(food=food1, ingredient=black_pepper, quantity="2 teaspoon")
    # food_ingredient11.save()
    # food_ingredient12 = FoodIngredient(food=food1, ingredient=tomato, quantity="6")
    # food_ingredient12.save()


