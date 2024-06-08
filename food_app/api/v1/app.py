from flask import Flask, request, jsonify
from flask_cors import CORS
from api.v1.views import app_views
from models import storage
from flask_jwt_extended import JWTManager
from datetime import timedelta


app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'a3f3217b1db812f16990d439'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

jwt = JWTManager()
jwt.init_app(app)

app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

with app.app_context():
    storage.reload()

@app.teardown_appcontext
def close_db(error):
    """ Close Storage """
    storage.close()

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': 'Not found'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)