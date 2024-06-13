from api.v1.views import app_views
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask import jsonify


@app_views.route('/refresh', methods=['POST'], strict_slashes=False)
@jwt_required(refresh=True)
def refresh():
    # Get the current user from the JWT
    current_user = get_jwt_identity()

    # Create a new access token
    access_token = create_access_token(identity=current_user)

    # Return the new access token
    return jsonify({'access_token': access_token}), 200

