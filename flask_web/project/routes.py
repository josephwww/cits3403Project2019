from flask import render_template, url_for, flash, redirect, request, abort
from project import app, db, bcrypt
from project.forms import RegistrationForm, LoginForm, UpdateAccountForm, PollForm
from project.models import User, Poll, Unit
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
def index():
	return redirect(url_for('home'))
@app.route("/home")
def home():
	
	return render_template('home.html',title='Home')

@app.route("/admin")
@login_required
def admin():
	if current_user.username != 'admin':
		abort(403)
	return render_template('admin.html',title='Admin')

@app.route("/poll",methods=['GET','POST'])
@login_required
def poll():
	form = PollForm()
	if form.validate_on_submit():
		poll=Poll(code=form.code.data, preferrence=form.preferrence.data, parti=current_user)
		db.session.add(poll)
		db.session.commit()
		flash(f'Voted successfully','success')
	#form.latter.choices = [(units.latter) for ]
	return render_template('poll.html',form = form, title='Poll')


@app.route("/about")
def about():
	return render_template('about.html',title='About')

@app.route("/register",methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'Your account has been created!','success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route("/login",methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password,form.password.data):
			login_user(user, remember=form.remember.data)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('home'))
		else:
			flash('Login unsuccessful.  Check you details!','danger')
	return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('home'))

@app.route("/account", methods=['GET','POST'])
@login_required
def account():
	form = UpdateAccountForm()
	if current_user.username == 'admin':
		return redirect(url_for('admin'))
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('your account has been updated!','success')
		return redirect(url_for('account'))
	return render_template('account.html', title='Account', form=form)

@app.route("/result")
def result():
	polls = Poll.query.all()
	return render_template('result.html',title='Result',polls=polls)
# @app.route("/poll/new", methods=['GET','POST'])
# @login_required
# def new_poll():
# 	form = PollForm()
# 	if form.validate_on_submit():
# 		poll = Poll(code=form.code.data, name=form.name.data, parti = current_user)
# 		flash('Poll contributed!','success')
# 		return redirect(url_for('home'))
# 	return render_template('create_poll.html', title='New Poll', form = form)


	 