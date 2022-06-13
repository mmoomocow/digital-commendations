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
		self.teacher = teacher_models.Teacher.objects.create(
			staff_code='Ab',
			house_group=teacher_models.Teacher.ANDERSON
		)
		# Then create 2 students
		self.student1 = student_models.Student.objects.create(
			id='23456',
			tutor_room='abc',
			house_group=student_models.Student.ANDERSON,
			year_level=student_models.Student.YEAR9,
		)
		self.student2 = student_models.Student.objects.create(
			id='34567',
			tutor_room='def',
			house_group=student_models.Student.BEGG,
			year_level=student_models.Student.YEAR9,
		)

		# Then create a commendation with the teachers and students linked
		self.commendation = commendation.objects.create(
			commendation_type=commendation.RESPECT,
			reason='Cupcake ipsum dolor sit amet sweet roll cheesecake jelly. Soufflé carrot cake sesame snaps toffee pie bears chocolate. Muffin halvah bonbon fruitcake marshmallow sweet roll.',
			teacher=self.teacher,
		)
		self.commendation.students.add(self.student1, self.student2)

	def test_commendation_creation(self):
		self.assertEqual(self.commendation.commendation_type, commendation.RESPECT, 'Commendation type is not correct')
		self.assertEqual(self.commendation.reason, 
			'Cupcake ipsum dolor sit amet sweet roll cheesecake jelly. Soufflé carrot cake sesame snaps toffee pie bears chocolate. Muffin halvah bonbon fruitcake marshmallow sweet roll.',
			'Commendation reason is not correct'
		)

	def test_commendation_links(self):
		self.assertEqual(self.commendation.teacher, self.teacher, 'Commendation teacher is not correct')
		self.assertEqual(self.commendation.students.count(), 2, 'Commendation students are not correct')
		self.assertEqual(str(self.commendation.students.first()), str(self.student1), 'Commendation student #1 is not correct')
		self.assertEqual(str(self.commendation.students.last()), str(self.student2), 'Commendation student #2 is not correct')
