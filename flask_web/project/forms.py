from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed #valiadator
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from package.models import User,Poll,Unit
from flask_login import login_user, current_user
from flask import flash
class RegistrationForm(FlaskForm):
	username = StringField("Username", validators=
		[DataRequired(),Length(min=2,max=20)])
	email = StringField("Email", validators=
		[DataRequired(),Email()])
	password = PasswordField("Password",validators=
		[DataRequired(),Length(min=8,max=20)])
	confirm_password = PasswordField("Confirm Password",validators=
		[DataRequired(),EqualTo('password')])
	submit = SubmitField("Sign up")

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError("Account existed already, plase use another username")

	def validate_email(self, email):
		email = User.query.filter_by(email=email.data).first()
		if email:
			raise ValidationError("Email existed already, plase use another email")

class LoginForm(FlaskForm):

	email = StringField("Email", validators=
		[DataRequired(),Email()])
	password = PasswordField("Password",validators=
		[DataRequired(),Length(min=8,max=20)])
	remember = BooleanField("Remember Me")

	submit = SubmitField("Sign in")


class UpdateAccountForm(FlaskForm):

	username = StringField("Username", validators=
		[DataRequired(),Length(min=2,max=20)])

	email = StringField("Email", validators=
		[DataRequired(),Email()])

	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png','jpeg'])])

	submit = SubmitField("Update")

	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError("Account existed already, plase use another username")

	def validate_email(self, email):
		if email.data != current_user.email:
			email = User.query.filter_by(email=email.data).first()
			if email:
				raise ValidationError("Email existed already, plase use another email")

class RequestResetForm(FlaskForm):

	email = StringField("Email", validators=
		[DataRequired(),Email()])

	submit = SubmitField("Request Password Reset")

	def validate_email(self, email):
		email = User.query.filter_by(email=email.data).first()
		if email is None:
			raise ValidationError("There seems to be no such email in our system.You must register first")

class ResetPasswordForm(FlaskForm):

	password = PasswordField("Password",validators=
		[DataRequired(),Length(min=8,max=20)])
	confirm_password = PasswordField("Confirm Password",validators=
		[DataRequired(),EqualTo('password')])

	submit = SubmitField("Reset Password")


class PollForm(FlaskForm):
	code = StringField('Unit Code',validators=[DataRequired(),Length(min=8,max=8)])
	preferrence = IntegerField('Preferrence(1~10, Use Integer!)', validators=[DataRequired(),NumberRange(min=1,max=10)])
	submit = SubmitField('VoteNow')
	#name = Unit.query.filter_by(code=code.data).first().name
	def validate_code(self, code):
		user = Poll.query.filter_by(code=code.data.upper(),user_id=current_user.id).first()
		unit = Unit.query.filter_by(code=code.data.upper()).first()


		if not unit:
			raise ValidationError('We do not have this unit!')

