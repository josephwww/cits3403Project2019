import os
import unittest

from package import app, db, bcrypt
from package.models import User, Poll

class TestCase(unittest.TestCase):
	def setUp(self):
		app.config['SECRET_KEY'] = '08424fa094ead1b004ff459bbd6e2750'
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
		self.app = app.test_client() 
		db.create_all()
		hashed_password = bcrypt.generate_password_hash('12345').decode('utf-8')
		u1 = User(username='user1',email='user1@unitsrank.xyz',password=hashed_password)
		u2 = User(username='user2',email='user2@unitsrank.xyz',password=hashed_password)
		db.session.add(u1)
		db.session.add(u2)
		db.session.commit()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_password_hashing(self):
		u=User.query.filter_by(username='user1').first()
		self.assertFalse(bcrypt.check_password_hash(u.password,'54321'))
		self.assertTrue(bcrypt.check_password_hash(u.password,'12345'))
		
	def test_is_poll_committed(self):
		p1 = Poll(code='CITS3403', preferrence=8, user_id=1)
		db.session.add(p1)
		db.session.commit()
		p=Poll.query.filter_by(code='CITS3403').first()
		self.assertTrue(p.preferrence==8)
		self.assertTrue(p.user_id==1)

	def test_home_page(self):
		response = self.app.get('/', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_register_page(self):
		response = self.app.get('/register', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_login_page(self):
		response = self.app.get('/login', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_about_page(self):
		response = self.app.get('/about', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_results_page(self):
		response = self.app.get('/results', follow_redirects=True)
		self.assertEqual(response.status_code, 200)


	def register(self, username,email, password, confirm_password):

		return self.app.post('/register',
			data=dict(username=username, email=email, 
				password=password, confirm_password=confirm_password),
			follow_redirects=True)

	def test_valid_user_registration(self):
		response = self.register('Hugo1','Hugo1@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
		self.assertEqual(response.status_code, 200)

	def test_invalid_user_registration_different_passwords(self):
		response = self.register('Hugo2','Hugo2@gmail.com', 'FlaskIsAwesome', 'FlaskIsNotAwesome')
		self.assertIn(b'Field must be equal to password.', response.data)

	def test_invalid_user_registration_duplicate_email(self):
		response = self.register('Hugo3','Hugo3@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
		self.assertEqual(response.status_code, 200)

	def login(self, email, password):
		return self.app.post(
			'/login',
			data=dict(email=email, password=password),
			follow_redirects=True
							)
	def logout(self):
		return self.app.get(
			'/logout',
			follow_redirects=True
			)





if __name__ == '__main__':
	unittest.main()
