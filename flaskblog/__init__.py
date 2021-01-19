from flask import Flask
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail,Message

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'project_user'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/project_user'
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config.from_pyfile('config.cfg')
mongo = PyMongo(app)

bcrypt = Bcrypt(app)
mail = Mail(app)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'

from flaskblog import routes