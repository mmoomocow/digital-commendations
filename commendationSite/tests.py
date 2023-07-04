from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.test import TestCase
from django.test.client import RequestFactory

from .authHelper import can_login, role_required
from .testHelper import createCaregiver, createStudent, createTeacher, createUser

# Create your tests here.

# General rules:
# - A user can only access a view if they are logged in
# - Only users with the assigned role can access the view
# - Superusers can access any view by default
# - If multiple roles are specified, the user can access the view if they are ANY of the roles


class TestAuthHelper(TestCase):
    def setUp(self):
        self.user = createUser(self)
        self.staff = createUser(self, is_staff=True)
        self.superuser = createUser(self, is_superuser=True)
        self.teacher = createTeacher(self)
        self.management = createTeacher(self, is_management=True)
        self.student = createStudent(self)
        self.caregiver = createCaregiver(self)
        self.anon = AnonymousUser()
        self.factory = RequestFactory()

    def test_student_required(self):
        @role_required(student=True)
        def testView(request):
            return HttpResponse("test")

        # Test that a student can access the view
        request = self.factory.get("/")
        request.user = self.student
        response = testView(request)
        self.assertEqual(response.status_code, 200)

        # Test that a teacher cannot access the view
        request = self.factory.get("/")
        request.user = self.teacher
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that a caregiver cannot access the view
        request = self.factory.get("/")
        request.user = self.caregiver
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that a staff cannot access the view
        request = self.factory.get("/")
        request.user = self.staff
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that a superuser can access the view
        request = self.factory.get("/")
        request.user = self.superuser
        response = testView(request)
        self.assertEqual(response.status_code, 200)

        # Test that a user cannot access the view
        request = self.factory.get("/")
        request.user = self.user
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that an anonymous user cannot access the view
        request = self.factory.get("/")
        request.user = self.anon
        with self.assertRaises(PermissionDenied):
            response = testView(request)

    def test_teacher_required(self):
        @role_required(teacher=True)
        def testView(request):
            return HttpResponse("test")

        # Test that a teacher can access the view
        request = self.factory.get("/")
        request.user = self.teacher
        response = testView(request)
        self.assertEqual(response.status_code, 200)

        # Test that a student cannot access the view
        request = self.factory.get("/")
        request.user = self.student
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that a caregiver cannot access the view
        request = self.factory.get("/")
        request.user = self.caregiver
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that a staff cannot access the view
        request = self.factory.get("/")
        request.user = self.staff
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that a superuser can access the view
        request = self.factory.get("/")
        request.user = self.superuser
        response = testView(request)
        self.assertEqual(response.status_code, 200)

        # Test that a user cannot access the view
        request = self.factory.get("/")
        request.user = self.user
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that an anonymous user cannot access the view
        request = self.factory.get("/")
        request.user = self.anon
        with self.assertRaises(PermissionDenied):
            response = testView(request)

    def test_management_required(self):
        @role_required(teacher=True, management=True)
        def testView(request):
            return HttpResponse("test")

        # Test that a teacher cannot access the view
        request = self.factory.get("/")
        request.user = self.teacher
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that a student cannot access the view
        request = self.factory.get("/")
        request.user = self.student
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that a caregiver cannot access the view
        request = self.factory.get("/")
        request.user = self.caregiver
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that a staff cannot access the view
        request = self.factory.get("/")
        request.user = self.staff
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that a superuser can access the view
        request = self.factory.get("/")
        request.user = self.superuser
        response = testView(request)
        self.assertEqual(response.status_code, 200)

        # Test that a user cannot access the view
        request = self.factory.get("/")
        request.user = self.user
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that an anonymous user cannot access the view
        request = self.factory.get("/")
        request.user = self.anon
        with self.assertRaises(PermissionDenied):
            response = testView(request)

    def test_caregiver_required(self):
        @role_required(caregiver=True)
        def testView(request):
            return HttpResponse("test")

        # Test that a teacher cannot access the view
        request = self.factory.get("/")
        request.user = self.teacher
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that a student cannot access the view
        request = self.factory.get("/")
        request.user = self.student
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that a caregiver can access the view
        request = self.factory.get("/")
        request.user = self.caregiver
        response = testView(request)
        self.assertEqual(response.status_code, 200)

        # Test that a staff cannot access the view
        request = self.factory.get("/")
        request.user = self.staff
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that a superuser can access the view
        request = self.factory.get("/")
        request.user = self.superuser
        response = testView(request)
        self.assertEqual(response.status_code, 200)

        # Test that a user cannot access the view
        request = self.factory.get("/")
        request.user = self.user
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that an anonymous user cannot access the view
        request = self.factory.get("/")
        request.user = self.anon
        with self.assertRaises(PermissionDenied):
            response = testView(request)

    def test_staff_required(self):
        @role_required(staff=True)
        def testView(request):
            return HttpResponse("test")

        # Test that a teacher cannot access the view
        request = self.factory.get("/")
        request.user = self.teacher
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that a student cannot access the view
        request = self.factory.get("/")
        request.user = self.student
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that a caregiver cannot access the view
        request = self.factory.get("/")
        request.user = self.caregiver
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that a staff can access the view
        request = self.factory.get("/")
        request.user = self.staff
        response = testView(request)
        self.assertEqual(response.status_code, 200)

        # Test that a superuser can access the view
        request = self.factory.get("/")
        request.user = self.superuser
        response = testView(request)
        self.assertEqual(response.status_code, 200)

        # Test that a user cannot access the view
        request = self.factory.get("/")
        request.user = self.user
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that an anonymous user cannot access the view
        request = self.factory.get("/")
        request.user = self.anon
        with self.assertRaises(PermissionDenied):
            response = testView(request)

    def test_superuser_required(self):
        @role_required(superuser=True)
        def testView(request):
            return HttpResponse("test")

        # Test that a teacher cannot access the view
        request = self.factory.get("/")
        request.user = self.teacher
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that a student cannot access the view
        request = self.factory.get("/")
        request.user = self.student
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that a caregiver cannot access the view
        request = self.factory.get("/")
        request.user = self.caregiver
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that a staff cannot access the view
        request = self.factory.get("/")
        request.user = self.staff
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that a superuser can access the view
        request = self.factory.get("/")
        request.user = self.superuser
        response = testView(request)
        self.assertEqual(response.status_code, 200)

        # Test that a user cannot access the view
        request = self.factory.get("/")
        request.user = self.user
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that an anonymous user cannot access the view
        request = self.factory.get("/")
        request.user = self.anon
        with self.assertRaises(PermissionDenied):
            response = testView(request)

    def test_teacher_student_required(self):
        @role_required(teacher=True, student=True)
        def testView(request):
            return HttpResponse("test")

        # Test that a teacher can access the view
        request = self.factory.get("/")
        request.user = self.teacher
        response = testView(request)
        self.assertEqual(response.status_code, 200)

        # Test that a student can access the view
        request = self.factory.get("/")
        request.user = self.student
        response = testView(request)
        self.assertEqual(response.status_code, 200)

        # Test that a caregiver cannot access the view
        request = self.factory.get("/")
        request.user = self.caregiver
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that a staff cannot access the view
        request = self.factory.get("/")
        request.user = self.staff
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that a superuser can access the view
        request = self.factory.get("/")
        request.user = self.superuser
        response = testView(request)
        self.assertEqual(response.status_code, 200)

        # Test that a user cannot access the view
        request = self.factory.get("/")
        request.user = self.user
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that an anonymous user cannot access the view
        request = self.factory.get("/")
        request.user = self.anon
        with self.assertRaises(PermissionDenied):
            response = testView(request)

    def test_teacher_caregiver_required(self):
        @role_required(teacher=True, caregiver=True)
        def testView(request):
            return HttpResponse("test")

        # Test that a teacher can access the view
        request = self.factory.get("/")
        request.user = self.teacher
        response = testView(request)
        self.assertEqual(response.status_code, 200)

        # Test that a student cannot access the view
        request = self.factory.get("/")
        request.user = self.student
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that a caregiver can access the view
        request = self.factory.get("/")
        request.user = self.caregiver
        response = testView(request)
        self.assertEqual(response.status_code, 200)

        # Test that a staff cannot access the view
        request = self.factory.get("/")
        request.user = self.staff
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that a superuser can access the view
        request = self.factory.get("/")
        request.user = self.superuser
        response = testView(request)
        self.assertEqual(response.status_code, 200)

        # Test that a user cannot access the view
        request = self.factory.get("/")
        request.user = self.user
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that an anonymous user cannot access the view
        request = self.factory.get("/")
        request.user = self.anon
        with self.assertRaises(PermissionDenied):
            response = testView(request)

    def test_student_caregiver_required(self):
        @role_required(student=True, caregiver=True)
        def testView(request):
            return HttpResponse("test")

        # Test that a teacher cannot access the view
        request = self.factory.get("/")
        request.user = self.teacher
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that a student can access the view
        request = self.factory.get("/")
        request.user = self.student
        response = testView(request)
        self.assertEqual(response.status_code, 200)

        # Test that a caregiver can access the view
        request = self.factory.get("/")
        request.user = self.caregiver
        response = testView(request)
        self.assertEqual(response.status_code, 200)

        # Test that a staff cannot access the view
        request = self.factory.get("/")
        request.user = self.staff
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that a superuser can access the view
        request = self.factory.get("/")
        request.user = self.superuser
        response = testView(request)
        self.assertEqual(response.status_code, 200)

        # Test that a user cannot access the view
        request = self.factory.get("/")
        request.user = self.user
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that an anonymous user cannot access the view
        request = self.factory.get("/")
        request.user = self.anon
        with self.assertRaises(PermissionDenied):
            response = testView(request)

    def test_staff_student_required(self):
        @role_required(staff=True, student=True)
        def testView(request):
            return HttpResponse("test")

        # Test that a teacher cannot access the view
        request = self.factory.get("/")
        request.user = self.teacher
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that a student can access the view
        request = self.factory.get("/")
        request.user = self.student
        response = testView(request)
        self.assertEqual(response.status_code, 200)

        # Test that a caregiver cannot access the view
        request = self.factory.get("/")
        request.user = self.caregiver
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that a staff can access the view
        request = self.factory.get("/")
        request.user = self.staff
        response = testView(request)
        self.assertEqual(response.status_code, 200)

        # Test that a superuser can access the view
        request = self.factory.get("/")
        request.user = self.superuser
        response = testView(request)
        self.assertEqual(response.status_code, 200)

        # Test that a user cannot access the view
        request = self.factory.get("/")
        request.user = self.user
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that an anonymous user cannot access the view
        request = self.factory.get("/")
        request.user = self.anon
        with self.assertRaises(PermissionDenied):
            response = testView(request)

    def test_teacher_NOT_superuser_required(self):
        @role_required(teacher=True, superuser=False)
        def testView(request):
            return HttpResponse("test")

        # Test that a teacher can access the view
        request = self.factory.get("/")
        request.user = self.teacher
        response = testView(request)
        self.assertEqual(response.status_code, 200)

        # Test that a student cannot access the view
        request = self.factory.get("/")
        request.user = self.student
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that a caregiver cannot access the view
        request = self.factory.get("/")
        request.user = self.caregiver
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that a staff cannot access the view
        request = self.factory.get("/")
        request.user = self.staff
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that a superuser cannot access the view
        request = self.factory.get("/")
        request.user = self.superuser
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that a user cannot access the view
        request = self.factory.get("/")
        request.user = self.user
        with self.assertRaises(PermissionDenied):
            response = testView(request)

        # Test that an anonymous user cannot access the view
        request = self.factory.get("/")
        request.user = self.anon
        with self.assertRaises(PermissionDenied):
            response = testView(request)

    def test_can_login(self):
        # Test that a user cannot login
        self.assertFalse(can_login(self.user))

        # Test that a staff member can login
        self.assertFalse(can_login(self.staff))

        # Test that a superuser can login
        self.assertTrue(can_login(self.superuser))

        # Test that a teacher can login
        self.assertTrue(can_login(self.teacher))

        # Test that a management teacher can login
        self.assertTrue(can_login(self.management))

        # Test that a student can login
        self.assertTrue(can_login(self.student))

        # Test that a caregiver can login
        self.assertFalse(can_login(self.caregiver))

        # Test that an anonymous user cannot login
        self.assertFalse(can_login(self.anon))
