from django.test import TestCase
from .models import *
from users import models as user_models

# Create your tests here.


class TeacherTestCase(TestCase):
    def setUp(self):
        # Create a teacher
        self.teacher = Teacher.objects.create(
            staff_code="Te", house_group=Teacher.ANDERSON
        )
        # Create a user object that can be linked to the teacher
        self.user = user_models.User.objects.create_user(
            username="teacher",
            email="teacher@example.com",
            password="teacherPassword",
            first_name="Teacher",
            last_name="User",
        )
        # Link the user to the teacher
        self.user.is_teacher = True
        self.user.teacher = self.teacher
        self.user.save()

        # Create a user to test permissions
        self.user2 = user_models.User.objects.create_user(
            username="notTeacher",
            email="notTeacher@example.com",
            password="notTeacherPassword",
            first_name="Not",
            last_name="Teacher",
        )

    def test_teacher_creation(self):
        self.assertEqual(self.teacher.staff_code, "Te", "Staff code is not correct")
        self.assertEqual(
            self.teacher.house_group, Teacher.ANDERSON, "House group is not correct"
        )
        self.assertEqual(
            str(self.teacher),
            "Te (Teacher User)",
            "Teacher string representation is not correct",
        )

    def test_user_link(self):
        # We don't need to test the full user because it is already tested in the UserTestCase
        self.assertEqual(
            self.user.teacher, self.teacher, "User is not linked to the teacher"
        )
        self.assertTrue(self.teacher.user.is_teacher, "Teacher is not a teacher")
        self.assertFalse(
            self.teacher.user.is_student, "Teacher should not be  a student"
        )
        self.assertFalse(
            self.teacher.user.is_caregiver, "Teacher should not be a caregiver"
        )
        self.assertEquals(
            str(self.teacher.user),
            "Teacher User",
            "User string representation is not correct",
        )

    def test_teacher_home(self):
        # Request will fail as not logged in
        response = self.client.get("/teachers/")
        self.assertEqual(
            response.status_code,
            403,
            "GET request to teacher home by unauthenticated users should be forbidden",
        )

        # Login as user
        self.client.login(username="notTeacher", password="notTeacherPassword")
        response = self.client.get("/teachers/")
        self.assertEqual(
            response.status_code,
            403,
            "GET request to teacher home by non-teachers should be forbidden",
        )
        self.client.logout()

        # Login as teacher
        self.client.login(username="teacher", password="teacherPassword")
        response = self.client.get("/teachers/")
        self.assertEqual(
            response.status_code,
            200,
            "GET request to teacher home by teachers should be successful",
        )
        self.assertTemplateUsed(
            response,
            "teachers/index.html",
            "Teacher home page should use the correct template",
        )
        self.assertTemplateUsed(
            response,
            "base.html",
            "Teacher home page should extend the base.html template",
        )
        self.client.logout()
