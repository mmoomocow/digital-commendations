from django.test import TestCase
from .models import *

# Create your tests here.

# Test the user model
class UserTestCase(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username='testuser',
			email='testUser@example.com',
			password='testpassword',
			first_name='Test',
			last_name='User',
		)
		self.superuser = User.objects.create_superuser(
			username='testSuperUser',
			email='testSuperUser@example.com',
			password='testpassword',
			first_name='Test',
			last_name='SuperUser',
		)
		self.webLogin = User.objects.create_user(
			username='testWebLogin',
			email='testWebLogin@example.com',
			password='testpassword',
			first_name='Test',
			last_name='WebLogin',
		)
		self.webLogin.is_teacher = True
		self.webLogin.save()

	def test_user_creation(self):
		self.assertEqual(self.user.username, 'testuser', 'Username is not correct')
		self.assertEqual(self.user.email, 'testUser@example.com', 'Email is not correct')
		self.assertTrue(self.user.check_password('testpassword'), 'Password is not correct')
		self.assertFalse(self.user.check_password('testpassword2'), 'Incorrect password was successful')
		self.assertEqual(self.user.first_name, 'Test', 'First name is not correct')
		self.assertEqual(self.user.last_name, 'User', 'Last name is not correct')
		self.assertEqual(str(self.user), 'Test User', 'User string representation is not correct')

	def test_superuser_creation(self):
		self.assertEqual(self.superuser.username, 'testSuperUser', 'Username is not correct')
		self.assertEqual(self.superuser.email, 'testSuperUser@example.com', 'Email is not correct')
		self.assertTrue(self.superuser.check_password('testpassword'), 'Password is not correct')
		self.assertFalse(self.superuser.check_password('testpassword2'), 'Incorrect password was successful')
		self.assertEqual(self.superuser.first_name, 'Test', 'First name is not correct')
		self.assertEqual(self.superuser.last_name, 'SuperUser', 'Last name is not correct')
		self.assertEqual(str(self.superuser), 'Test SuperUser', 'User string representation is not correct')

	def test_user_permissions(self):
		self.assertFalse(self.user.is_staff, 'User is staff')
		self.assertFalse(self.user.is_superuser, 'User is superuser')
		self.assertTrue(self.user.is_active, 'User is not active')

	def test_superuser_permissions(self):
		self.assertTrue(self.superuser.is_staff, 'Superuser is not staff')
		self.assertTrue(self.superuser.is_superuser, 'Superuser is not superuser')
		self.assertTrue(self.superuser.is_active, 'Superuser is not active')

	def test_user_login(self):
		response1 = self.client.post('/users/login/', data={'username': 'testWebLogin', 'password': 'testpassword'})
		self.assertEqual(response1.status_code, 202, 'Correct username and password was not accepted')
		response2 = self.client.post('/users/login/', data={'username': 'testWebLogin', 'password': 'testpassword2'})
		self.assertEqual(response2.status_code, 403, 'Incorrect username and password was accepted')
		response3 = self.client.post('/users/login/', data={'username': 'testuser', 'password': 'testpassword'})
		self.assertEqual(response3.status_code, 403, 'Non teacher user was logged in')