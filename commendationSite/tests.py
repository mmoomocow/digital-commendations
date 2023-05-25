from django.http import HttpResponse
from django.test import TestCase

from .authHelper import teacher_required
from .testHelper import createTeacher, createUser

# Create your tests here.


class TestAuthHelper(TestCase):
    def setUp(self):
        self.user = createUser(self)
        self.teacher = createTeacher(self)

        self.fake_view = teacher_required()(lambda request: HttpResponse("Test"))
        self.fake_view_management = teacher_required(is_management=True)(
            lambda request: HttpResponse("Test")
        )

    def test_teacherRequired_noAuth(self):
        with self.assertRaises(Exception):
            request = self.client.get("/").wsgi_request
            _ = self.fake_view(request)

    def test_teacherRequired_notTeacher(self):
        # Log in as a user that is not a teacher
        self.client.login(username=self.user.username, password="password")
        with self.assertRaises(Exception):
            request = self.client.get("/").wsgi_request
            _ = self.fake_view(request)

    def test_teacherRequired_teacher(self):
        # Log in as a teacher
        self.client.login(username=self.teacher.username, password="password")
        request = self.client.get("/").wsgi_request
        response = self.fake_view(request)

        # Test that the decorator returns a 200 when the user is a teacher
        self.assertEqual(
            response.status_code,
            200,
            "Teacher auth check did not return 200 for teacher user",
        )

    def test_managementRequired_teacher(self):
        # Log in as a teacher
        self.client.login(username=self.teacher.username, password="password")
        with self.assertRaises(Exception):
            request = self.client.get("/").wsgi_request
            _ = self.fake_view_management(request)

    def test_managementRequired_management(self):
        # Log in as a management teacher
        self.teacher.teacher.is_management = True
        self.teacher.teacher.save()
        self.client.login(username=self.teacher.username, password="password")
        request = self.client.get("/").wsgi_request
        response = self.fake_view_management(request)

        # Test that the decorator returns a 200 when the user is a management teacher
        self.assertEqual(
            response.status_code,
            200,
            "Teacher auth check with is_management did not return 200 for management teacher user",
        )

    def tearDown(self):
        self.client.logout()
