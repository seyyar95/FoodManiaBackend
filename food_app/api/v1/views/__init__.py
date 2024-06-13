from flask import Blueprint

# Create a Blueprint object named app_views
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import all the views
from api.v1.views.users import *
from api.v1.views.jwt_refresh import *
from api.v1.views.foods import *