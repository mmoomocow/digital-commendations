from django.test import TestCase
from commendationSite import testHelper
from .models import User
from teachers.models import Teacher
from students.models import Student, Caregiver

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

    def test_login_get(self):
        testHelper.get_page(self, "/users/login/", "users/login.html")

    def test_login_get_authenticated(self):
        # Test login with a already logged in
        self.client.force_login(self.teacher)
        testHelper.get_page(
            self,
            "/users/login/",
            "users/login.html",
            check_templates=False,
            status_code=302,
        )

    def test_login_post(self):
        # Test that a user can log in
        testHelper.post_page(
            self,
            "/users/login/",
            data={
                "username": self.teacher.username,
                "password": "password",
            },
            status_code=302,
        )

    def test_login_post_inactive(self):
        # Test that an inactive user cannot log in
        self.teacher.is_active = False
        self.teacher.save()

        testHelper.post_page(
            self,
            "/users/login/",
            data={
                "username": self.teacher.username,
                "password": "password",
            },
            status_code=403,
        )

    def test_login_post_wrong_password(self):
        # Test login with the wrong password
        testHelper.post_page(
            self,
            "/users/login/",
            data={
                "username": self.teacher.username,
                "password": "wrong_password",
            },
            status_code=403,
        )

    def test_login_post_wrong_username(self):
        # Test login with the wrong username
        testHelper.post_page(
            self,
            "/users/login/",
            data={
                "username": "wrong_username",
                "password": "password",
            },
            status_code=403,
        )

    def test_login_post_student(self):
        # Test that a student cannot log in
        testHelper.post_page(
            self,
            "/users/login/",
            data={
                "username": self.student.username,
                "password": "password",
            },
            status_code=403,
        )

    def test_login_next(self):
        # Test that a user can log in and be redirected to the next page specified in the url
        request = self.client.post(
            "/users/login/?next=/teachers/",
            data={
                "username": self.teacher.username,
                "password": "password",
            },
            follow=True,
        )
        # Check redirected to the next page
        self.assertRedirects(request, "/teachers/")

    def test_logout_authenticated(self):
        # Test that a user can log out
        self.client.force_login(self.teacher)
        testHelper.get_page(
            self,
            "/users/logout/",
            "users/logout.html",
            check_templates=False,
            status_code=302,
        )

    def test_logout_next(self):
        # Test that a user can log out and be redirected to the next page specified in the url
        self.client.force_login(self.teacher)
        request = self.client.get(
            "/users/logout/?next=/users/login/",
            follow=True,
        )
        # Check redirected to the next page
        self.assertRedirects(request, "/users/login/")

    def test_logout_unauthenticated(self):
        # Test that no user doesn't cause an error
        testHelper.get_page(
            self,
            "/users/logout/",
            "users/logout.html",
            check_templates=False,
            status_code=302,
        )

    def tearDown(self):
        pass  # nothing to tear down as database is reset after each test
