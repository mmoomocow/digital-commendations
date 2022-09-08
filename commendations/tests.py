from django.test import TestCase
from .models import Commendation, Milestone
from commendationSite import testHelper

# Create your tests here.


class commendationsTest(TestCase):
    def setUp(self):
        self.teacher = testHelper.createTeacher(self, is_management=False)
        self.student = testHelper.createStudent(self)
        self.client.login(username=self.teacher.username, password="password")

    def test_giveCommendation_get(self):
        testHelper.testPage(self, "/commendations/award/", "commendations/award.html")

    def test_giveCommendation_post(self):
        data = {
            "commendationType": "E",
            "reason": "Test",
            "students": [self.student.student.id],
            "teacher": self.teacher.id,
        }

        # Post the commendation
        page = self.client.post("/commendations/award/", data=data)
        self.assertEqual(
            page.status_code,
            302,
            f"Page /commendations/award/ returned {page.status_code} instead of 302",
        )

        # Check that the commendation was created
        commendation = Commendation.objects.filter(
            commendation_type="E",
            reason="Test",
            teacher=self.teacher.teacher.id,
            students=self.student.student.id,
        )
        self.assertTrue(
            commendation.exists(),
            f"Commendation was not created, expected {data}, got {commendation}",
        )
    def tearDown(self):
        pass
