from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask import jsonify
from api.v1.views import app_views

@app_views.route('/refresh', methods=['POST'], strict_slashes=False)
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify({'access_token': access_token}), 200


# @jwt.expired_token_loader
# def expired_token_callback():
#     return jsonify({'message': 'The token has expired'}), 401