import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail #mail server port 
from flask_admin import Admin


app = Flask(__name__)
app.config["SECRET_KEY"] = '3125b5bb0e3dd8a6095a1247c14fc735'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db'
db =SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app) #add funtionality into our db model
login_manager.login_view = 'login' 
login_manager.login_message_category = "info "
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'hugozhang0521@gmail.com'
app.config['MAIL_PASSWORD'] = 'LJQ520..'
mail = Mail(app)
admin = Admin(app)




from package import routes