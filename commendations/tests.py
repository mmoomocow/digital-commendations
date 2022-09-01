from django.test import TestCase
from .models import Commendation
from users import models as user_models
from students import models as student_models
from teachers import models as teacher_models

# Create your tests here.


class CommendationTestCase(TestCase):
    def setUp(self):
        # Commendation needs teachers and students
        # First create a teacher
        self.teacher = user_models.User.objects.create_user(
            username="CommendationTeacher",
            email="testTeacher@example.com",
            password="teacherpassword",
            first_name="Commendation",
            last_name="Teacher",
        )
        self.teacher.is_teacher = True
        self.teacher.teacher = teacher_models.Teacher.objects.create(
            staff_code="Ab",
            house_group=teacher_models.Teacher.ANDERSON,
        )
        self.teacher.save()

        # Then create 2 students
        self.student1 = user_models.User.objects.create_user(
            username="CommendationStudent1",
            email="commendationStudent1@example.com",
            password="studentpassword",
            first_name="Commendation",
            last_name="Student1",
        )
        self.student1.is_student = True
        self.student1.student = student_models.Student.objects.create(
            id="23456",
            tutor_room="abc",
            house_group=student_models.Student.BEGG,
            year_level=student_models.Student.YEAR9,
        )
        self.student1.save()

        self.student2 = user_models.User.objects.create_user(
            username="CommendationStudent2",
            email="commendationStudent2@example.com",
            password="studentpassword",
            first_name="Commendation",
            last_name="Student2",
        )
        self.student2.is_student = True
        self.student2.student = student_models.Student.objects.create(
            id="34567",
            tutor_room="def",
            house_group=student_models.Student.BEGG,
            year_level=student_models.Student.YEAR9,
        )
        self.student2.save()

        # Then create a commendation with the teachers and students linked
        self.commendation = Commendation.objects.create(
            commendation_type=Commendation.RESPECT,
            reason="Cupcake ipsum dolor sit amet sweet roll cheesecake jelly. Soufflé carrot cake sesame snaps toffee pie bears chocolate. Muffin halvah bonbon fruitcake marshmallow sweet roll.",
            teacher=self.teacher.teacher,
        )
        self.commendation.students.add(self.student1.student, self.student2.student)

        # Create a user that's not a teacher to test permissions
        self.user = user_models.User.objects.create_user(
            username="CommendationUser",
            email="commendationUser@example.com",
            password="userpassword",
            first_name="Commendation",
            last_name="User",
        )

    def test_commendation_creation(self):
        self.assertEqual(
            self.commendation.commendation_type,
            Commendation.RESPECT,
            "Commendation type is not correct",
        )
        self.assertEqual(
            self.commendation.reason,
            "Cupcake ipsum dolor sit amet sweet roll cheesecake jelly. Soufflé carrot cake sesame snaps toffee pie bears chocolate. Muffin halvah bonbon fruitcake marshmallow sweet roll.",
            "Commendation reason is not correct",
        )

    def test_commendation_links(self):
        self.assertEqual(
            self.commendation.teacher,
            self.teacher.teacher,
            "Commendation teacher is not correct",
        )
        self.assertEqual(
            self.commendation.students.count(),
            2,
            "Commendation students are not correct",
        )
        # The order of students is not important or guaranteed, so we only check if both students are in the list
        self.assertTrue(
            self.commendation.students.contains(self.student1.student),
            "Commendation student #1 is not correct",
        )
        self.assertTrue(
            self.commendation.students.contains(self.student2.student),
            "Commendation student #2 is not correct",
        )

    def test_commendation_str(self):
        self.assertEqual(
            str(self.commendation),
            "Commendation ID: 1",
            "Commendation string is not correct",
        )

    def test_award_commendation_get(self):
        # Request will fail as not logged in
        response = self.client.get("/commendations/award/")
        self.assertEqual(
            response.status_code,
            403,
            "GET request to award commendation by unauthenticated users should be forbidden",
        )

        # Login as user
        self.client.login(username="CommendationUser", password="userpassword")
        response = self.client.get("/commendations/award/")
        self.assertEqual(
            response.status_code,
            403,
            "GET request to award commendation by non-teachers should be forbidden",
        )
        self.client.logout()

        # Login as a teacher
        self.client.login(username="CommendationTeacher", password="teacherpassword")
        response = self.client.get("/commendations/award/")
        self.assertEqual(
            response.status_code,
            200,
            "GET request to award commendation by teachers should be successful",
        )
        self.assertTemplateUsed(
            response, "commendations/award.html", "Award commendation template not used"
        )
        self.assertTemplateUsed(
            response, "base.html", "Award commendation did not extend base.html"
        )
        # reset client
        self.client.logout()

    def test_award_commendation_post(self):
        # Request will fail as not logged in
        response = self.client.post("/commendations/award/")
        self.assertEqual(
            response.status_code,
            403,
            "POST request to award commendation by unauthenticated users should be forbidden",
        )
        # Login as a teacher
        self.client.login(username="CommendationTeacher", password="teacherpassword")
        response = self.client.post(
            "/commendations/award/",
            {
                "commendationType": Commendation.RESPECT,
                "reason": "Post request test",
                "teacher": self.teacher.teacher.id,
                "students": [self.student1.student.id, self.student2.student.id],
            },
        )
        self.assertEqual(response.status_code, 302)
        newCommendation = Commendation.objects.get(
            commendation_type=Commendation.RESPECT,
            reason="Post request test",
        )
        self.assertEqual(newCommendation.teacher, self.teacher.teacher)
        self.assertEqual(newCommendation.students.count(), 2)
        self.assertTrue(newCommendation.students.contains(self.student1.student))
        self.assertTrue(newCommendation.students.contains(self.student2.student))

        # reset client
        self.client.logout()
