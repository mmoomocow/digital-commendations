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

    def test_Commendation(self):
        commendation = Commendation.objects.create(
            commendation_type="E",
            reason="Test",
            teacher=self.teacher.teacher,
        )
        commendation.students.add(self.student.student)

        # Check that the commendation was created and has the correct values
        self.assertEqual(
            commendation.commendation_type,
            "E",
            f"Commendation type was not set correctly, expected E, got {commendation.commendation_type}",
        )

        self.assertEqual(
            commendation.reason,
            "Test",
            f"Commendation reason was not set correctly, expected Test, got {commendation.reason}",
        )

        self.assertEqual(
            commendation.teacher,
            self.teacher.teacher,
            f"Commendation teacher was not set correctly, expected {self.teacher.teacher}, got {commendation.teacher}",
        )

        self.assertEqual(
            commendation.students.first(),
            self.student.student,
            f"Commendation student was not set correctly, expected {self.student.student}, got {commendation.students.first()}",
        )

    def test_Milestone(self):
        milestone = Milestone.objects.create(
            milestone_type=Milestone.GREEN,
            student=self.student.student,
        )

        # Check that the milestone was created and has the correct values
        self.assertEqual(
            milestone.milestone_type,
            Milestone.GREEN,
            f"Milestone type was not set correctly, expected {Milestone.GREEN}, got {milestone.milestone_type}",
        )

        self.assertEqual(
            milestone.student,
            self.student.student,
            f"Milestone student was not set correctly, expected {self.student.student}, got {milestone.student}",
        )

        self.assertFalse(
            milestone.awarded,
            f"Milestone awarded was not set correctly, expected False, got {milestone.awarded}",
        )

        # test the prettyPrint method
        self.assertEqual(
            milestone.prettyPrint(),
            "Green Jr School spirit badge - 50 commendations",
            f"Milestone prettyPrint was not set correctly, expected Green, got {milestone.prettyPrint()}",
        )

    def tearDown(self):
        self.client.logout()
