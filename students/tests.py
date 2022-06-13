from django.test import TestCase
from .models import *
from users import models as user_models

# Create your tests here.

class StudentCaregiverTestCase(TestCase):
	def setUp(self):
		# TODO - Create a caregiver and link to the student
		# Create a student
		self.student = Student.objects.create(
			id='12345',
			tutor_room='abc',
			house_group=Student.ANDERSON,
			year_level=Student.YEAR9,
		)
		# Create a user object that can be linked to the student
		self.user = user_models.User.objects.create_user(
			username='student',
			email='student@example.com',
			password='studentpassword',
			first_name='Student',
			last_name='User',
		)
		# Link the user to the student
		self.user.is_student = True
		self.user.student = self.student
		self.user.save()

	def test_student_creation(self):
		self.assertEqual(self.student.id, '12345', 'Student ID is not correct')
		self.assertEqual(self.student.tutor_room, 'ABc', 'Tutor room is not correct')
		self.assertEqual(self.student.house_group, Student.ANDERSON, 'House group is not correct')
		self.assertEqual(self.student.year_level, Student.YEAR9, 'Year level is not correct')
		self.assertEqual(str(self.student), '12345', 'Student string representation is not correct')

	def test_user_link(self):
		# We don't need to test the full user because it is already tested in the UserTestCase
		self.assertEqual(self.user.student, self.student, 'User is not linked to the teacher')
		self.assertTrue(self.student.user.is_student, 'Student should be  a student')
		self.assertFalse(self.student.user.is_teacher, 'Student should not be a teacher')
		self.assertFalse(self.student.user.is_caregiver, 'Student should not be a caregiver')
		self.assertEquals(str(self.student.user), 'Student User', 'User string representation is not correct')
