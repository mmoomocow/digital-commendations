from django.test import TestCase
from users.models import User
from teachers.models import Teacher
from students.models import Student
import random

# Helper functions for testing


def testPage(self: TestCase, path: str, template: str):
    """_summary_: Tests a page to see if it returns a 200 status code and uses the correct template

    Args:
        self (TestCase): The test case
        path (str): The path to test
        template (str): The template to test for
    """
    page = self.client.get(path)
    self.assertEqual(
        page.status_code, 200, f"Page {path} returned {page.status_code} instead of 200"
    )
    self.assertTemplateUsed(page, "base.html", f"Page {path} did not use base.html")
    self.assertTemplateUsed(page, template, f"Page {path} did not use {template}")


# Create a user with garbage data
def createUser(_self: TestCase) -> User:
    """_summary_: Creates a user with garbage data

    Args:
        _self (TestCase): The test case

    Returns:
        User: The user that was created
    """
    user = User.objects.create_user(
        username="".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10)),
        email="".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10)),
        password="password",
        first_name="Test",
        last_name="User",
    )
    return user


# Create a teacher and link it to a user
def createTeacher(_self: TestCase, is_management: bool = False) -> User:
    """_summary_: Creates a teacher and links it to a user

    Args:
        _self (TestCase): The test case
        is_management (bool, optional): Should the teacher be management?. Defaults to False.

    Returns:
        User: The user that was created
    """
    user = createUser(_self)
    teacher = Teacher.objects.create(
        staff_code="".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=2)),
        user=user,
        is_management=is_management,
    )
    user.teacher = teacher
    user.is_teacher = True
    user.save()
    return user


# Create a student and link it to a user
def createStudent(_self: TestCase) -> User:
    """_summary_: Creates a student and links it to a user

    Args:
        _self (TestCase): The test case

    Returns:
        User: The user that was created
    """
    user = createUser(_self)
    student = Student.objects.create(
        id=random.randint(10000, 99999),
        tutor_room="".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=2)),
        house_group=Student.ANDERSON,
    )
    user.student = student
    user.is_student = True
    user.save()
    return user
