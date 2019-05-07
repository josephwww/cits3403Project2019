from datetime import datetime
from project import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    polls = db.relationship('Poll', backref='parti', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"

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

