from flask import Flask, render_template,url_for,flash,redirect, request
from package.forms import (RegistrationForm, LoginForm, 
UpdateAccountForm, RequestResetForm, ResetPasswordForm, PollForm)
from package.models import User, Poll, Unit
from package import app, db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
import secrets, os
from PIL import Image
from flask_mail import Message

# @app.route('/favicon.ico')
# def favicon():
# 	return redirect(url_for('static', filename='favicon.ico'),code=302)
	
@app.route("/")
@app.route("/home")
def home():
	return render_template("home.html")

@app.route("/about")
def about():
	return render_template("about.html")


@app.route("/register", methods=["GET", "POST"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f"Account created for {form.username.data}, Log in now!", "success")
		return redirect(url_for('login'))
	return render_template("register.html", title="Register", form = form)

@app.route("/login", methods=["GET","POST"])
def login():
	form = LoginForm()
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and user.is_admin: #admin login
			if form.password.data == user.password:
				login_user(user, remember=form.remember.data)
				flash("you have been logged in!","success")
				return redirect(url_for("admin.index"))

			else:
				flash("check you credentials","danger")

		elif user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)#normal user login
			next_page = request.args.get('next')
			flash("you have been logged in!","success")
			return redirect(next_page) if next_page else redirect(url_for("home"))
		else:
			flash("check you credentials","danger")
	return render_template("login.html", title="Login", form = form)

@app.route("/logout")
@login_required
def logout():
	logout_user()
	flash(f'Log out successfully!',"success")
	return redirect(url_for('home'))

def save_picture(form_picture):
	random_hex = secrets.token_hex(8)
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	picture_path = os.path.join(app.root_path, 'static/img',picture_fn)

	#resize image

	output_size = (250,250)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	i.save(picture_path)
	return picture_fn


@app.route("/account", methods=["GET","POST"])
@login_required

def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file

		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash(f"Your account has been updated", "success")
		return redirect(url_for('account'))

	elif request.method =="GET": #fill the current username and email by default
		form.username.data = current_user.username
		form.email.data = current_user.email

	image_file = url_for('static', filename="img/" + current_user.image_file)
	return render_template("account.html", title='account', 
		image_file=image_file, form=form)

def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request', 
		sender='noreply@demo.com', 
		recipients=[user.email])

	msg.body = f''' To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}


If you did not make this request, then simply igonore this email and no change will be made
''' #multiline strings absolute url _external
	mail.send(msg)


@app.route("/reset_password", methods=["GET","POST"])
def reset_request():
	if current_user.is_authenticated:
		flash(f'Please log out before reset password')
		return redirect(url_for('home'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash("An email has been sent with instructions to reset your password. Remember to check the bin", 'info')
		return redirect(url_for('login'))
	return render_template('reset_request.html', title='Reset Password', form=form)	


@app.route("/reset_password/<token>", methods=["GET","POST"])
def reset_token(token):
	if current_user.is_authenticated:
		flash(f'Please log out before reset the password')
		return redirect(url_for('home'))	
	user = User.verify_reset_token(token)
	if user is None:
		flash(f"That is an invalid or expired token", "warning")
		return redirect(url_for('reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
		user.password = hashed_password
		db.session.commit()
		flash(f"Your password has been updated", "success")
		return redirect(url_for('login'))
	return render_template('reset_token.html', title='Reset Password', form=form)	


@app.route("/vote",methods=['GET','POST'])
@login_required
def vote():
	form = PollForm()
	if form.validate_on_submit():
		code=form.code.data.upper()
		user_poll = Poll.query.filter_by(code=code, user_id=current_user.id).first()
		if user_poll:
			user_poll.preferrence = form.preferrence.data
			db.session.commit()
			flash(f'You cannot vote twice for the same unit, but your new preferrence has been updated','danger')
			return redirect(url_for('result'))

		else:
			poll=Poll(code=code, preferrence=form.preferrence.data, parti=current_user)
			db.session.add(poll)
			db.session.commit()
			flash(f'Voted successfully','success')
			return redirect(url_for('result'))
	#form.latter.choices = [(units.latter) for ]
	return render_template('vote.html',form = form, title='vote')

@app.route("/results", methods=["GET"])
def result():
	polls = db.engine.execute(" SELECT code, ROUND(AVG(preferrence),1)  AS a , count(preferrence) AS b  FROM poll GROUP BY code HAVING b>1  ORDER BY a DESC LIMIT 10")
	return render_template('results.html',title='Result',polls=polls)

