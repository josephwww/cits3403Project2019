# cits3403Project2019

# design and development of the application
  The application provides five main fuctions to the users, which are Registration, Log in, Vote, Result, Admin.
  Firstly, user needs to register a account and log in. The username and email are unique in the sqlite database.
# instructions to launch the applictaion
  python3 run.py
# dependencies (i.e. required modules)
  -Flask
  -Flask-Admin
  -Flask-Bcrypt
  -Flask-Login
  -Flask-Mail
  -Flask-SQLAlchemy
  -Flask-WTF
# admin
  Adding a adminisitration account is not directly from the website,
  But through running 'sqlite3 site.db' for safty reason
  SQL Script:
  INSERT INTO user ('username','email','image_file','password','is_admin')
  VALUES('YOUR_USER_NAME','YOUR_EMAIL','default.jpg','YOUR_PASSWORD',TRUE)
# testing
