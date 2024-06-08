from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.users import *
from api.v1.views.jwt_refresh import *
from api.v1.views.foods import *