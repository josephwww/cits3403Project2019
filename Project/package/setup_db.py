from datetime import datetime
from flask_login import UserMixin, current_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_admin.contrib.sqla import ModelView
from flask import url_for, redirect
#reloading the user from the user id stored in the session
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail #mail server port 
from flask_admin import Admin


app = Flask(__name__)
app.config["SECRET_KEY"] = '3125b5bb0e3dd8a6095a1247c14fc735'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.db'
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

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(20), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
	password = db.Column(db.String(60), nullable=False)
	is_admin = db.Column(db.Boolean, default=False)
	poll = db.relationship('Poll', backref='parti', lazy=True)

	def __repr__(self):
		return f"User('{self.username}','{self.email}','{self.image_file}')"

	def get_reset_token(self, expires_sec=1800):
		s = Serializer(app.config["SECRET_KEY"], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod #not to expect self
	def verify_reset_token(token):
		s = Serializer(app.config["SECRET_KEY"]) 
		try:
			auser_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)

class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(8), nullable=False)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Unit('{self.name}')"

class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(8), nullable=False)
    date_polled = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    preferrence = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Poll('{self.code}','{self.name}')"

class MyModelView(ModelView):

	def is_accessible(self):
		if current_user.is_admin:
			return current_user.is_authenticated
		else:
			return abort(404)
	def inaccessible_callback(self, name, **kwargs):
		return redirect(url_for('login'))


admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Poll, db.session))
