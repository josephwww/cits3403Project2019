# cits3403Project2019
Author:22289267 HONGFENG WANG 22037457 CHANGAN ZHANG
        
# design and development of the application
The application provides five main fuctions to the users, which are Registration, Log in, Vote, Result, Admin.
At the about page, we provide ajax javascript to view the result without redirecting.
Firstly, user needs to register a account and log in. The username and email are unique in the sqlite database. In case of forgetting the password, we provide reseeting password through the email.
User logs in  to the website with their own credential, otherwise they will be introduced to registration page.
The vote section requires logged in user. User simply input the unit code in UWA and their preference toward the unit. The unit code occupies eight characters and the website would check the availability of the unit code(i.e. Is the unit existed in UWA?). Once the preference has been submitted, their contribution towards the same unit will only change the preference in the database without creating a new record.
The result is according to the preference contributed by the participants. It simply gets the average of each unit and rank it in descending order. We only show the units that have been voted twice or more.
Everyone has access to the result page. This page provides the view of all units have been voted by preference in descending order with how many participants. Additionally, The bar graph under each unit  shows the data in an easy way.
In the admin section, with the administration account logged in, we can delete, create, upload the user detail and users' vote.
# Instructions to launch the applictaion
  Within the project file
  execute:
  python3 run.py
  And should be available to visit by browser using localhost:5000
# Dependencies (i.e. required modules)
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
  unittest:
  python3 test.py
