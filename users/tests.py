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

	def test_user_creation(self):
		self.assertEqual(self.user.username, 'testuser', 'Username is not correct')
		self.assertEqual(self.user.email, 'testUser@example.com', 'Email is not correct')
		self.assertTrue(self.user.check_password('testpassword'), 'Password is not correct')
		self.assertFalse(self.user.check_password('testpassword2'), 'Incorrect password was successful')
		self.assertEqual(self.user.first_name, 'Test', 'First name is not correct')
		self.assertEqual(self.user.last_name, 'User', 'Last name is not correct')
		self.assertEqual(str(self.user), 'Test User', 'User string representation is not correct')

	def test_user_permsissions(self):
		self.assertFalse(self.user.is_staff, 'User is staff')
		self.assertFalse(self.user.is_superuser, 'User is superuser')
		self.assertTrue(self.user.is_active, 'User is not active')
