from flask import Flask, request, jsonify
from flask_cors import CORS
from api.v1.views import app_views
from models import storage
from flask_jwt_extended import JWTManager


app = Flask(__name__)
# app.config['SECRET_KEY'] = 'H-FQNSzB6au14y_XEq3YKa7L8jSmqI7n'
app.config['JWT_SECRET_KEY'] = 'a3f3217b1db812f16990d439'
# app.config["JWT_ALGORITHM"] = "HS256"

jwt = JWTManager()
jwt.init_app(app)

app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

with app.app_context():
    storage.reload()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)