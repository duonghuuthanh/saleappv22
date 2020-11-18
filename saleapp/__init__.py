from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager
import os

app = Flask(__name__)
app.secret_key = 'kjif7346873249047287e&^#@&^%#'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/saledbv2?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.config['ROOT_PROJECT_PATH'] = app.root_path



db = SQLAlchemy(app=app)
admin = Admin(app=app,
              name='IT81 SHOP 2',
              template_mode='bootstrap4')
login = LoginManager(app=app)