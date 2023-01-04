import os

class Config(object):
     SECRET_KEY = os.environ.get('SECRET_KEY') or 'secrectkey123'
     # MYSQL_HOST = 'localhost'
     # MYSQL_USER = 'root'
     # MYSQL_PASSWORD = ''
     # MYSQL_DB = 'test'
     SQLALCHEMY_DATABASE_URI = 'mysql://root:''@localhost/finalproject'
     SQLALCHEMY_TRACK_MODIFICATIONS = False
     UPLOAD_FOLDER = 'static\\files'