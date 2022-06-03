from django.db import models

# Create your models here.

class commendation(models.Model):
	"""
	The commendations that will be given to students as a reward

	This model contains will contain data about the commendation, who gave it
	who it was given to, the commendation type and the reason for giving it
	"""

	# Unique id for commendations
	id = models.AutoField(primary_key=True, unique=True, editable=False, blank=False, null=False, verbose_name='ID')

	# The type of commendation given
	RESPECT = 'R'
	INTEGRITY = 'I'
	SERVICE = 'S'
	EXCELLENCE = 'E'
	OTHER = 'O'
	COMMENDATION_TYPE_CHOICES = (
		(RESPECT, 'Respect'),
		(INTEGRITY, 'Integrity'),
		(SERVICE, 'Service'),
		(EXCELLENCE, 'Excellence'),
		(OTHER, 'Other'),
	)
	commendation_type = models.CharField(max_length=1, choices=COMMENDATION_TYPE_CHOICES, blank=False, null=False, verbose_name='Commendation Type')

	# The reason for giving the commendation
	reason = models.TextField(max_length=500, blank=False, null=False, verbose_name='Reason')

	# The date and time the commendation was given
	date_time = models.DateTimeField(blank=False, null=False, verbose_name='Date and Time given', auto_now_add=True)

	# The teacher who gave the commendation
	teacher = models.ForeignKey('teachers.teacher', on_delete=models.CASCADE, blank=False, null=False, verbose_name='Teacher')

	# The student(s) who received the commendation
	students = models.ManyToManyField('students.student', blank=False, verbose_name='Students')

	class Meta:
		verbose_name = 'Commendation'
		verbose_name_plural = 'Commendations'

	def __str__(self):
		return 'Commendation ID: {}'.format(self.id)
