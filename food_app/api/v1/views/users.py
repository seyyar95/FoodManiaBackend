from api.v1.views import app_views
from flask import jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from email_validator import validate_email, EmailNotValidError
from models.users import User
from models.foodsave import FoodSave 
from models import storage
import os

@app_views.route('/register',  methods=['POST'], strict_slashes=False)
def register():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    try:
        valid_email = validate_email(email)
    except EmailNotValidError as e:
        return jsonify({'error': str(e)}), 400

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
    
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    
    return jsonify(
        {
            "access": access_token,
            "refresh": refresh_token
        }
    ), 200


@app_views.route('/update',  methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_user():
    data = request.get_json()
    user_id = get_jwt_identity()
    profile_pictrue = request.file['profile_pic']
    

    user = storage.get_by_id(User, user_id)
    
    if data.get('name'):
        user.name = data.get('name')
    if data.get('email'):
        user.email = data.get('email')
    if data.get('password'):
        user.set_password(data.get('password'))
    if profile_pictrue:
        filename = secure_filename(profile_pictrue.filename)

        profile_pictrue.save(os.path.join(app.config['PROFILE_PICTURES'], filename))
        
        user.profile_pic = filename + "_" + str(user.id)
    user.save()

    return jsonify({'message': 'User updated successfully'}), 200
