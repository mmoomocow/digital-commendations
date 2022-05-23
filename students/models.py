from django.db import models

# Create your models here.

class Caregiver(models.Model):
	pass

class Student(models.Model):
	"""
		The model for students.

		This model will link to commendations, and contain data that is
		specific to students only, and therefore not suitable for the
		generic user model.
	"""

	# The KAMAR assigned student ID is a unique identifier for the student
	id = models.IntegerField(unique=True, blank=False, null=False, verbose_name='Student ID')

	# The student's tutor room
	tutor_room = models.CharField(max_length=3, blank=False, null=False, verbose_name='Tutor Room')
	# The student's house group
	house_group = models.Choices((('Anderson', 'Anderson'), ('Begg', 'Begg'), ('Ross', 'Ross'), ('Herron', 'Herron'), ('Somerville', 'Somerville')))
	# The student's year level
	year_level = models.IntegerChoices((9, 'Year 9'), (10, 'Year 10'), (11, 'Year 11'), (12, 'Year 12'), (13, 'Year 13'))

	# Parent/caregiver
	caregiver = models.foreignKey(Caregiver, on_delete=models.CASCADE, verbose_name='Parent/Caregiver')
