from flask import Blueprint

datamanager = Blueprint('datamanager', __name__,url_prefix = '/data', template_folder='templates', static_folder='static')

from app.datamanager import router