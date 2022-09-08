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


    def test_viewMilestones_get(self):
        self.teacher.teacher.is_management = True
        self.teacher.teacher.save()
        testHelper.testPage(
            self, "/commendations/spirit/", "commendations/award_milestones.html"
        )
        self.teacher.teacher.is_management = False
        self.teacher.teacher.save()

    def test_viewMilestones_post(self):
        self.teacher.teacher.is_management = True
        self.teacher.teacher.save()

        milestone = Milestone.objects.create(
            milestone_type=Milestone.GREEN,
            student=self.student.student,
        )

        data = {
            "milestone": milestone.id,
        }

        # Post the milestone
        page = self.client.post("/commendations/spirit/", data=data)
        self.assertEqual(
            page.status_code,
            302,
            f"Page /commendations/spirit/ returned {page.status_code} instead of 302",
        )

        # Check that the milestone has been marked as awarded
        milestone = Milestone.objects.get(id=milestone.id)
        self.assertTrue(
            milestone.awarded,
            f"Milestone was not awarded, expected {data}, got {milestone}",
        )

        self.teacher.teacher.is_management = False
        self.teacher.teacher.save()

    def tearDown(self):
        pass
