from django.db import models

# Create your models here.

class Teacher(models.Model):
	"""
		The model for teachers and staff.

		This model will link to commendations, and contain data that is 
		specific to staff members only, and therefore not suitable for the
		generic user model.

		The generic user model contains all of the basic information that
		is required for a user to log in, and contains email address, name
		password etc, so this information should not be stored in the teacher model
	"""

	# Teacher ID
	# Used internally to uniquely identify teachers
	id = models.AutoField(primary_key=True, unique=True, editable=False, blank=False, null=False, verbose_name='ID')

	# Staff code
	# Uniquely identifies the teacher but can be repeated once a teacher has left the school.
	staff_code = models.CharField(max_length=2, unique=True, blank=False, null=False, verbose_name='Staff Code')

	# House group
	house_group = models.Choices((('Anderson', 'Anderson'), ('Begg', 'Begg'), ('Ross', 'Ross'), ('Herron', 'Herron'), ('Somerville', 'Somerville')))

	class Meta:
		ordering = ('staff_code',)

	def __str__(self):
		return self.staff_code

	def delete(self, *args, **kwargs):
		# Delete the teacher
		super().delete(*args, **kwargs)
