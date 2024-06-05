from api.v1.views import app_views
from flask import jsonify
from models.users import User
from models import storage

@app_views.route('/status', strict_slashes=False)
def status():
    new_dict = {'name': 'Useer', 'email': 'exampl@gmail.com', 'password_has': '123456'}
    new_user = User(**new_dict)
    # new_user.set_password(new_user.password_hash)
    new_user.save()
    # users = storage.all(User).values()
    # return jsonify([user.to_dict() for user in users])
    user = [new_user.to_dict()]
    return jsonify(user), 200