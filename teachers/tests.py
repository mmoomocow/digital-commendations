import random

from django.test import TestCase

from commendationSite import testHelper

from .models import Teacher

# Create your tests here.


class teachersTest(TestCase):
    def setUp(self) -> None:
        self.teacher = testHelper.createTeacher(self, is_management=True)
        self.client.login(username=self.teacher.username, password="password")

    def test_Teacher(self):
        teacher = testHelper.createTeacher(self)
        teacher2 = Teacher.objects.create(
            staff_code="".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=2)),
        )

        self.assertEqual(Teacher.objects.get(id=teacher.teacher.id), teacher.teacher)

        # Test __str__ method
        self.assertEqual(
            str(self.teacher.teacher),
            f"{self.teacher.teacher.staff_code} ({self.teacher.first_name} {self.teacher.last_name})",
        )

        self.assertEqual(str(teacher2), f"{teacher2.staff_code}")

    def tearDown(self):
        self.client.logout()


class teachersViewsTest(TestCase):
    def setUp(self) -> None:
        self.teacher = testHelper.createTeacher(self, is_management=True)
        self.client.login(username=self.teacher.username, password="password")

    def test_index(self):
        testHelper.get_page(self, "/teachers/", "teachers/index.html")
