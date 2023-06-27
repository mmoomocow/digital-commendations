import random

from django.test import TestCase

from commendationSite import testHelper

from .models import Student

# Create your tests here.


class studentsModelTest(TestCase):
    def setUp(self):
        self.student = testHelper.createStudent(self)
        self.teacher = testHelper.createTeacher(self, is_management=True)
        self.user = testHelper.createUser(self)

        self.client.login(username=self.teacher.username, password="password")

    def test_Student(self):
        # Create a student and check it exists
        student = testHelper.createStudent(self)
        self.assertEqual(Student.objects.get(id=student.student.id), student.student)

    def test_student_str(self):
        student2 = Student.objects.create(
            id=random.randint(10000, 99999),
            tutor_room="".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=2)),
            house_group=Student.ANDERSON,
        )
        # Test __str__ method
        self.assertEqual(
            str(self.student.student),
            f"{self.student.first_name} {self.student.last_name} ({self.student.student.id})",
        )

        # Student with no user
        self.assertEqual(str(student2), f"{student2.id}")

    def tearDown(self):
        self.client.logout()


class studentsViewsTest(TestCase):
    def setUp(self):
        self.student = testHelper.createStudent(self)
        self.teacher = testHelper.createTeacher(self, is_management=True)
        self.user = testHelper.createUser(self)

        self.client.login(username=self.teacher.username, password="password")

    def test_listStudents(self):
        testHelper.get_page(self, "/students/list/", "students/list_students.html")
        # Test with a search query
        testHelper.get_page(
            self, "/students/list/?search=Test", "students/list_students.html"
        )

    def test_studentInfo(self):
        testHelper.get_page(
            self,
            f"/students/list/{self.student.student.id}/",
            "students/student_info.html",
        )

    def test_studentInfo_404(self):
        # Test that a student that doesn't exist returns a 404
        # As using handler404 checking status code will not work
        testHelper.get_page(
            self, f"/students/list/{self.student.student.id + 1}/", "errors/404.html"
        )

    def test_student_home(self):
        # Login as a student and check they can access their home page
        self.client.force_login(self.student)
        testHelper.get_page(
            self,
            f"/students/",
            "students/student_home.html",
        )

    def test_student_home_not_student(self):
        # Login as a teacher and check they can't access the student home page
        self.client.force_login(self.teacher)
        testHelper.get_page(
            self,
            f"/students/",
            "errors/403.html",
        )
