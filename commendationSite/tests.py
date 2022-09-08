from django.test import TestCase
from .authHelper import teacher_required
from .testHelper import createTeacher, createUser
from django.http import HttpResponse


# Create your tests here.


class TestAuthHelper(TestCase):
    def setUp(self):
        self.user = createUser(self)
        self.teacher = createTeacher(self)

    def test_teacher_required(self):
        # Create a fake view to test the decorator
        @teacher_required()
        def fake_view(request):
            return HttpResponse("Test")

        # Create a request with an unauthenticated user
        request = self.client.get("/").wsgi_request
        response = fake_view(request)

        # Test that the decorator returns a 401 when there is no user
        response = fake_view(request)
        self.assertEqual(
            response.status_code,
            401,
            "Teacher auth check did not return 401 for unauthenticated user",
        )

        # Log in as a user that is not a teacher
        self.client.login(username=self.user.username, password="password")
        request = self.client.get("/").wsgi_request
        response = fake_view(request)

        # Test that the decorator returns a 403 when the user is not a teacher
        self.assertEqual(
            response.status_code,
            403,
            "Teacher auth check did not return 403 for non-teacher user",
        )

        # Log in as a teacher
        self.client.login(username=self.teacher.username, password="password")
        request = self.client.get("/").wsgi_request
        response = fake_view(request)

        # Test that the decorator returns a 200 when the user is a teacher
        self.assertEqual(
            response.status_code,
            200,
            "Teacher auth check did not return 200 for teacher user",
        )

        # Recreate the view but require is_management
        @teacher_required(is_management=True)
        def fake_view(request):
            return HttpResponse("Test")

        # Test that the decorator returns a 403 when the user is not a management teacher
        response = fake_view(request)
        self.assertEqual(
            response.status_code,
            403,
            "Teacher auth check with is_management did not return 403 for non-management teacher user",
        )

        # Log in as a management teacher
        self.teacher.teacher.is_management = True
        self.teacher.teacher.save()
        self.client.login(username=self.teacher.username, password="password")
        request = self.client.get("/").wsgi_request
        response = fake_view(request)

        # Test that the decorator returns a 200 when the user is a management teacher
        self.assertEqual(
            response.status_code,
            200,
            "Teacher auth check with is_management did not return 200 for management teacher user",
        )

    def tearDown(self):
        self.client.logout()
