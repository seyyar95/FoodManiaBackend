from api.v1.views import app_views
from flask import jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token
from models.users import User
from models import storage
from models.foodsave import FoodSave 


@app_views.route('/register',  methods=['POST'], strict_slashes=False)
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name:
        return jsonify({'error': 'Name is required'}), 400
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    if not password:
        return jsonify({'error': 'Password is required'}), 400
    
    existing_user = User.get_user_by_email(email)
    if existing_user:
        return jsonify({'error': 'Email already in use'}), 403    

    new_user = User(name=name, email=email)
    new_user.set_password(password)

    new_user.save()
    return jsonify({'message': 'User created successfully'}), 201

 
@app_views.route('/login',  methods=['POST'], strict_slashes=False)
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email:
        return jsonify({'error': 'Email is required'}), 400
    if not password:
        return jsonify({'error': 'Password is required'}), 400
    
    user = User.get_user_by_email(email)
    if user is None or not user.check_password(password):
        return jsonify({'error': 'Invalid email or password'}), 400
    
    access_token = create_access_token(identity=user.name)
    refresh_token = create_refresh_token(identity=user.name)
    
    
    return jsonify(
        {
            "access": access_token,
            "refresh": refresh_token
        }
    ), 200
    