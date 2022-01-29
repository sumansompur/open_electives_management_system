import imp
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'
bcrypt = Bcrypt(app)
#login_manager = LoginManager(app)
#login_manager.login_view = "login_page"
#login_manager.login_message_category = "info"
from OEMS import routes

config = {
  'user': 'sumanlokesh',
  'password': 'Suman123',
  'host': 'localhost',
  'database': 'open_electives',
  'raise_on_warnings': True
}

db = mysql.connector.connect(**config)
cursor = db.cursor()



