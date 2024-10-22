from datetime import timedelta
import random
from flask import Flask, request, jsonify
from flask_cors import CORS
from api.v1.views import app_views
from models.daily_suggest import DailySuggestion
from models.foods import Food
from models import storage
from flask_jwt_extended import JWTManager
from threading import Thread
import time
import os

"""
    Create a Flask app
"""
app = Flask(__name__)

# Set the secret key to sign the JWTs
app.config['JWT_SECRET_KEY'] = 'a3f3217b1db812f16990d439'

# Set the JWT expiration time
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=1)

# Set the JWT refresh token expiration time
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)


# Create a JWTManager object
jwt = JWTManager()
jwt.init_app(app)

# Enable CORS
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})



# app context to reload storage
with app.app_context():
    storage.reload()

# Error handling for missing JWT token
@jwt.expired_token_loader
def expired_token_callback(expired_token, exception):
    return jsonify({'message': 'The token has expired'}), 401

# Close storage
@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()

# Custom error handler for 404 (Not found) errors
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': 'Not found'}), 404


def update_suggest():
    suggested_foods = storage.all(DailySuggestion)
    for food in suggested_foods.values():
        food.delete()
    
    while True:
        daily_foods  = list(storage.all(Food).values())
        suggested_foods: list[DailySuggestion] = list()
        foods = random.sample(daily_foods, 10)
        for food in foods:
            new = DailySuggestion(food_id=food.id)
            new.save()
            suggested_foods.append(new)
        time.sleep(10)
        for food in suggested_foods:
            food.delete()
    


# Running Flask application
def run():
    update = Thread(target=update_suggest)
    update.start()
    app.register_blueprint(app_views)
    app.run(host='0.0.0.0', port=5000, threaded=True)
