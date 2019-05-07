from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired,Length, Email, EqualTo, ValidationError, NumberRange
from project.models import User, Poll, Unit

class RegistrationForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
	email = StringField('Email',validators=[DataRequired(),Email()])
	password = PasswordField('Password',validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password')])
	submit = SubmitField('Sign up')

	def validate_username(self,username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Username already exist!')

	def validate_email(self,email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('email already exist, try login!')

class LoginForm(FlaskForm):
	email = StringField('Email',validators=[DataRequired(),Email()])
	password = PasswordField('Password',validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Log in')

class UpdateAccountForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired(),Length(min=2,max=20)])
	email = StringField('Email',validators=[DataRequired(),Email()])
	submit = SubmitField('Update')

	def validate_username(self,username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('Username already exist!')

	def validate_email(self,email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('email already exist, try login!')

class PollForm(FlaskForm):
	code = StringField('Unit Code(CAPITAL LETTER, PLZ!)',validators=[DataRequired(),Length(min=8,max=8)])
	preferrence = IntegerField('Preferrence(-5~5, Integer!)', validators=[DataRequired(),NumberRange(min=-5,max=5)])
	submit = SubmitField('Poll')
	#name = Unit.query.filter_by(code=code.data).first().name
	def validate_code(self,code):
		user=Poll.query.filter_by(code=code.data,user_id=current_user.id).first()
		if user:
			raise ValidationError('You have voted this unit!')
