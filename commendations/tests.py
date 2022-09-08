from django.test import TestCase
from .models import Commendation, Milestone
from commendationSite import testHelper

# Create your tests here.

class commendationsTest(TestCase):
    def setUp(self):
        self.teacher = testHelper.createTeacher(self, is_management=False)
        self.student = testHelper.createStudent(self)
        self.client.login(username=self.teacher.username, password="password")

    def tearDown(self):
        pass
