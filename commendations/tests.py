from django.test import TestCase
from .models import *
from users import models as user_models
from students import models as student_models
from teachers import models as teacher_models

# Create your tests here.

class CommendationTestCase(TestCase):
	def setUp(self):
		# Commendation needs teachers and students
		# First create a teacher
		self.teacher = user=user_models.User.objects.create_user(
				username='CommendationTeacher',
				email='testTeacher@example.com',
				password='teacherpassword',
				first_name='Commendation',
				last_name='Teacher',
			)
		self.teacher.is_teacher = True
		self.teacher.teacher = teacher_models.Teacher.objects.create(
			staff_code='Ab',
			house_group=teacher_models.Teacher.ANDERSON,
		)
		self.teacher.save()

		# Then create 2 students
		self.student1 = user_models.User.objects.create_user(
			username='CommendationStudent1',
			email='commendationStudent1@example.com',
			password='studentpassword',
			first_name='Commendation',
			last_name='Student1',
		)
		self.student1.is_student = True
		self.student1.student=student_models.Student.objects.create(
			id='23456',
			tutor_room='abc',
			house_group=student_models.Student.BEGG,
			year_level=student_models.Student.YEAR9,
		)
		self.student1.save()

		self.student2 = user_models.User.objects.create_user(
			username='CommendationStudent2',
			email='commendationStudent2@example.com',
			password='studentpassword',
			first_name='Commendation',
			last_name='Student2',
		)
		self.student2.is_student = True
		self.student2.student=student_models.Student.objects.create(
			id='34567',
			tutor_room='def',
			house_group=student_models.Student.BEGG,
			year_level=student_models.Student.YEAR9,
		)
		self.student2.save()

		# Then create a commendation with the teachers and students linked
		self.commendation = commendation.objects.create(
			commendation_type=commendation.RESPECT,
			reason='Cupcake ipsum dolor sit amet sweet roll cheesecake jelly. Soufflé carrot cake sesame snaps toffee pie bears chocolate. Muffin halvah bonbon fruitcake marshmallow sweet roll.',
			teacher=self.teacher.teacher,
		)
		self.commendation.students.add(self.student1.student, self.student2.student)

	def test_commendation_creation(self):
		self.assertEqual(self.commendation.commendation_type, commendation.RESPECT, 'Commendation type is not correct')
		self.assertEqual(self.commendation.reason, 
			'Cupcake ipsum dolor sit amet sweet roll cheesecake jelly. Soufflé carrot cake sesame snaps toffee pie bears chocolate. Muffin halvah bonbon fruitcake marshmallow sweet roll.',
			'Commendation reason is not correct'
		)

	def test_commendation_links(self):
		self.assertEqual(self.commendation.teacher, self.teacher.teacher, 'Commendation teacher is not correct')
		self.assertEqual(self.commendation.students.count(), 2, 'Commendation students are not correct')
		# The order of students is not important or guaranteed, so we only check if both students are in the list
		self.assertTrue(self.commendation.students.contains(self.student1.student), 'Commendation student #1 is not correct')
		self.assertTrue(self.commendation.students.contains(self.student2.student), 'Commendation student #2 is not correct')
