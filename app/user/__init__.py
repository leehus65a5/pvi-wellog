from flask import Blueprint

user = Blueprint('user', __name__, url_prefix = '/user', template_folder='templates', static_folder='static')

from app.user import router