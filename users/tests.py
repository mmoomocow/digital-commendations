from django.test import TestCase

from commendationSite import testHelper
from students.models import Caregiver, Student
from teachers.models import Teacher

from .models import User

# Create your tests here.


class UserModelTest(TestCase):
    def setUp(self):
        self.teacher = testHelper.createTeacher(self, is_management=True)
        self.student = testHelper.createStudent(self)
        self.user = testHelper.createUser(self)

    def test_user(self):
        self.assertEqual(User.objects.get(id=self.user.id).username, self.user.username)
        self.assertEqual(
            str(self.user), f"{self.user.first_name} {self.user.last_name}"
        )

    def test_deleteTeacher(self):
        # Create a teacher with a linked user
        teacher = testHelper.createTeacher(self, is_management=True)
        # Delete the user and check that the teacher is deleted
        teacher.delete()
        self.assertEqual(Teacher.objects.filter(id=teacher.teacher.id).count(), 0)

    def test_deleteStudent(self):
        # Create a student with a linked user
        student = testHelper.createStudent(self)
        # Delete the user and check that the student is deleted
        student.delete()
        self.assertEqual(Student.objects.filter(id=student.student.id).count(), 0)

    def test_deleteCaregiver(self):
        # Create a caregiver with a linked user
        caregiver = testHelper.createCaregiver(self)
        # Delete the user and check that the caregiver is deleted
        caregiver.delete()
        self.assertEqual(Caregiver.objects.filter(id=caregiver.caregiver.id).count(), 0)

    def test_deleteUser(self):
        # Create a user
        user = testHelper.createUser(self)
        # Delete the user and check that the user is deleted
        user.delete()
        self.assertEqual(User.objects.filter(id=user.id).count(), 0)


class UserViewsTest(TestCase):
    def setUp(self):
        self.teacher = testHelper.createTeacher(self, is_management=True)
        self.student = testHelper.createStudent(self)
        self.user = testHelper.createUser(self)

    def test_login_redirect(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 301)
        response = self.client.get("/login/", follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")

    def test_login_get(self):
        response = self.client.get("/users/login/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")

    def test_login_post_valid(self):
        response = self.client.post(
            "/users/login/",
            {"username": self.teacher.username, "password": "password"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")
        self.assertEqual(response.wsgi_request.user, self.teacher)

    def test_login_post_invalid(self):
        response = self.client.post(
            "/users/login/",
            {"username": self.teacher.username, "password": "wrong"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login/")
        self.assertEqual(response.wsgi_request.user.is_authenticated, False)

    def test_login_not_allowed(self):
        response = self.client.post(
            "/users/login/",
            {"username": self.student.username, "password": "password"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login/")
        self.assertEqual(response.wsgi_request.user.is_authenticated, False)

    def test_logout(self):
        self.client.force_login(self.teacher)
        response = self.client.get("/users/logout/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")
        self.assertEqual(response.wsgi_request.user.is_authenticated, False)
