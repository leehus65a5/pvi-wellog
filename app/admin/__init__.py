from flask import Blueprint

admin = Blueprint('admin', __name__,  url_prefix='/admin', template_folder='templates', static_folder='static')

from app.admin import router