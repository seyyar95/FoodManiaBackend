from api.v1.views import app_views
from flask import jsonify, current_app, request
from models.users import User
from models import storage


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
    storage.new(new_user)
    storage.save()
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
    
    return jsonify({'message': 'Login successful'}), 200
    