from api.v1.views import app_views
from flask import jsonify, request, current_app
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from api.v1 import app
from werkzeug.utils import secure_filename
from email_validator import validate_email, EmailNotValidError
from models.users import User
from models.foodsave import FoodSave 
from models import storage
import os

@app_views.route('/register',  methods=['POST'], strict_slashes=False)
def register():
    # Get the data from the request
    data = request.get_json()
    name = data.get('name').strip()
    email = data.get('email').strip()

    # Validate the email
    try:
        valid_email = validate_email(email)
    except EmailNotValidError as e:
        return jsonify({'error': str(e)}), 400

    # Get the password from the request
    password = data.get('password')

    # Return an error if the name, email, or password is not provided
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    if not password:
        return jsonify({'error': 'Password is required'}), 400
    
    # Check if the email is already in use
    existing_user = User.get_user_by_email(email)
    if existing_user:
        return jsonify({'error': 'Email already in use'}), 403    

    # Create a new user
    new_user = User(name=name, email=email)
    new_user.set_password(password)

    # Save the user to the database
    new_user.save()
     # Create an access token and a refresh token
    access_token = create_access_token(identity=new_user.id)
    refresh_token = create_refresh_token(identity=new_user.id)
    
    # Return the access and refresh tokens
    return jsonify(
        {
            "access": access_token,
            "refresh": refresh_token
        }
    ), 201

 
@app_views.route('/login',  methods=['POST'], strict_slashes=False)
def login():
    # Get the data from the request
    data = request.get_json()
    email = data.get('email').strip()
    password = data.get('password')

    # Return an error if the email or password is not provided
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    if not password:
        return jsonify({'error': 'Password is required'}), 400
    
    # Get the user by email
    user = User.get_user_by_email(email)

    # Return an error if the user is not found or the password is incorrect
    if user is None or not user.check_password(password):
        return jsonify({'error': 'Invalid email or password'}), 400
    
    # Create an access token and a refresh token
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    # Return the access and refresh tokens
    return jsonify(
        {
            "access": access_token,
            "refresh": refresh_token
        }
    ), 200


@app_views.route('/update',  methods=['GET', 'PATCH'], strict_slashes=False)
@jwt_required()
def update_user():
    # Get the data from the request
    user_id = get_jwt_identity()
    
    # Get the user by id
    user = storage.get_by_id(User, user_id)
    
    if request.method == 'PATCH':
        data = request.get_json()
    
    
        # Update fields if provided in the request data
        if data.get('name'):
            user.name = data.get('name')
        if data.get('email'):
            user.email = data.get('email')
        if data.get('password'):
            user.set_password(data.get('password'))
        user.save()

    return jsonify({
        'name': user.name,
        'email': user.email,
    }), 200


@app_views.route('/health')
def healt_check():
    return "SALAM GAGA", 200