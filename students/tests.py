from django.test import TestCase
from commendationSite import testHelper
from .models import Student
import random

# Create your tests here.

# Models to test
# - Student
# Views to test
# - listStudents
# - studentInfo


class studentsTest(TestCase):
    def setUp(self):
        self.student = testHelper.createStudent(self)
        self.teacher = testHelper.createTeacher(self, is_management=True)
        self.user = testHelper.createUser(self)

        self.client.login(username=self.teacher.username, password="password")

    def test_listStudents(self):
        testHelper.testPage(self, "/students/", "students/list_students.html")
        # Test with a search query
        testHelper.testPage(
            self, "/students/?search=Test", "students/list_students.html"
        )

    def test_studentInfo(self):
        testHelper.testPage(
            self, f"/students/{self.student.student.id}/", "students/student_info.html"
        )
        # Test that a student that doesn't exist returns a 404
        req = self.client.get(f"/students/{self.student.student.id + 1}/")
        self.assertEqual(req.status_code, 404)

    def test_Student(self):
        # Create a student and check it exists
        student = testHelper.createStudent(self)
        student2 = Student.objects.create(
            id=random.randint(10000, 99999),
            tutor_room="".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=2)),
            house_group=Student.ANDERSON,
        )
        self.assertEqual(Student.objects.get(id=student.student.id), student.student)

        # Test __str__ method
        self.assertEqual(
            str(self.student.student),
            f"{self.student.first_name} {self.student.last_name} ({self.student.student.id})",
        )

        self.assertEqual(str(student2), f"{student2.id}")

    def tearDown(self):
        pass
