from unittest.mock import patch

from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.test import RequestFactory, TestCase

from commendationSite import testHelper
from students.models import Caregiver, Student
from teachers.models import Teacher

from .backends import TENANT_DOMAIN, MicrosoftAuthBackend
from .models import User
from .views import callback, login

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
        self.request_factory = RequestFactory()
        self.teacher = testHelper.createTeacher(self, is_management=True)
        self.student = testHelper.createStudent(self)
        self.caregiver = testHelper.createCaregiver(self)
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
        self.assertEqual(response.url, "/portal/")
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
            {"username": self.user.username, "password": "password"},
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

    def test_successful_callback(self):
        def mock_login(request, user):
            """Mock login function"""
            request.session["user_id"] = user.id

        with patch("users.views.django_authenticate", return_value=self.teacher) as MA:
            # with patch("users.views.django_login", side_effect=mock_login) as ML:
            response = self.client.get(
                "/users/callback/?code=123&state=456", follow=True
            )
        self.assertTrue(MA.called)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_no_backend(self):
        # Remove the MicrosoftAuthBackend from the settings and test that login and callback return ImproperlyConfigured
        with self.settings(AUTHENTICATION_BACKENDS=[]):
            with self.assertRaises(ImproperlyConfigured):
                self.client.get("/users/login/")
            with self.assertRaises(ImproperlyConfigured):
                self.client.get("/users/callback/")

    def test_login_already_authenticated(self):
        self.client.force_login(self.teacher)
        response = self.client.get("/users/login/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/portal/")

    def test_login_no_credentials(self):
        response = self.client.post("/users/login/", {}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")
        self.assertContains(response, "Please enter both username and password.")
        self.assertEqual(response.wsgi_request.user.is_authenticated, False)

    def test_login_inactivated_user(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.post(
            "/users/login/",
            {"username": self.user.username, "password": "password"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login.html")
        self.assertEqual(response.wsgi_request.user.is_authenticated, False)

    def test_logout_not_authenticated(self):
        response = self.client.get("/users/logout/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_callback_no_code(self):
        response = self.client.get("/users/callback/")
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login/")


class MockResponse:
    def __init__(self, json_data, status_code=200):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


class MicrosoftAuthBackendTest(TestCase):
    def setUp(self):
        self.backend = MicrosoftAuthBackend()
        self.request_factory = RequestFactory()
        self.user = User.objects.create_user(
            username="johndoe",
            password="password",
            is_active=True,
            is_teacher=True,
            email=f"johndoe@{TENANT_DOMAIN}",
            first_name="John",
            last_name="Doe",
        )

    def test_setup(self):
        request = self.request_factory.get("/")
        request.session = {}
        self.backend.setup(request)
        self.assertIsNotNone(request.session.get(self.backend.SESSION_KEY))
        self.assertIsNotNone(request.session[self.backend.SESSION_KEY].get("flow"))

    def test_get_auth_uri(self):
        request = self.request_factory.get("/")
        request.session = {}
        auth_uri = self.backend.get_auth_uri(request)
        self.assertTrue(auth_uri.startswith("https://login.microsoftonline.com"))

    def test_authenticate_successful(self):
        # Simulate a successful authentication request
        user_data = {
            "givenName": self.user.first_name,
            "surname": self.user.last_name,
            "mail": self.user.email,
            "id": "dummy_id",
        }
        access_token = "dummy_access_token"
        request = self.request_factory.get("/")
        request.GET = {"code": "dummy_code"}
        request.session = {
            self.backend.SESSION_KEY: {"flow": {"dummy_key": "dummy_value"}}
        }  # Update the value to a dictionary

        # Mock the requests.get method to return the user data
        def mock_get(url, headers):
            return MockResponse(user_data)

        # Patch the ms_client.acquire_token_by_auth_code_flow method
        with patch.object(
            self.backend.ms_client,
            "acquire_token_by_auth_code_flow",
            return_value={"access_token": access_token},
        ):
            with patch("requests.get", side_effect=mock_get):
                user = self.backend.authenticate(request)

        # Assert the user and user data
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "johndoe")
        self.assertEqual(user.email, f"johndoe@{TENANT_DOMAIN}")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")

    def test_authenticate_no_code(self):
        # Simulate an authentication request without a code
        request = self.request_factory.get("/")
        request.GET = {}
        request.session = {
            self.backend.SESSION_KEY: {"flow": {"dummy_key": "dummy_value"}}
        }

        user = self.backend.authenticate(request)

        # Assert that no user is returned
        self.assertIsNone(user)

    def test_authenticate_no_flow(self):
        # Simulate an authentication request without a flow
        request = self.request_factory.get("/")
        request.GET = {"code": "dummy_code"}
        request.session = {}

        user = self.backend.authenticate(request)

        # Assert that no user is returned
        self.assertIsNone(user)

    def test_authenticate_invalid_token(self):
        # Simulate an authentication request with an invalid token
        request = self.request_factory.get("/")
        request.GET = {"code": "dummy_code"}
        request.session = {self.backend.SESSION_KEY: {"flow": "dummy_flow"}}

        # Mock the ms_client.acquire_token_by_auth_code_flow method to raise a ValueError
        with patch.object(
            self.backend.ms_client,
            "acquire_token_by_auth_code_flow",
            side_effect=ValueError,
        ):
            user = self.backend.authenticate(request)
            self.assertIsNone(user)

    def test_authenticate_invalid_email(self):
        # Simulate a successful authentication request
        user_data = {
            "givenName": "John",
            "surname": "Doe",
            "mail": f"johndoe@invalid.com",
        }
        access_token = "dummy_access_token"
        request = self.request_factory.get("/")
        request.GET = {"code": "dummy_code"}
        request.session = {
            self.backend.SESSION_KEY: {"flow": {"dummy_key": "dummy_value"}}
        }  # Update the value to a dictionary

        # Mock the requests.get method to return the user data
        def mock_get(url, headers):
            return MockResponse(user_data)

        # Patch the ms_client.acquire_token_by_auth_code_flow method
        with patch.object(
            self.backend.ms_client, "acquire_token_by_auth_code_flow"
        ) as mock_acquire_token:
            mock_acquire_token.return_value = {"access_token": access_token}
            with patch("requests.get", side_effect=mock_get):
                user = self.backend.authenticate(request)

        # Assert the user and user data
        self.assertIsNone(user)
