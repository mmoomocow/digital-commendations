from django.test import TestCase
from users.models import User
from teachers.models import Teacher
from students.models import Student, Caregiver
import random

# Helper functions for testing


def get_page(
    self: TestCase,
    path: str,
    template: str = None,
    check_templates: bool = True,
    status_code: int = 200,
):
    """_summary_: Tests a page to see if it returns a 200 status code and uses the correct template

    Args:
        self (TestCase): The test case
        path (str): The path to test
        template (str): The template to test for
    """
    page = self.client.get(path)
    self.assertEqual(
        page.status_code,
        status_code,
        f"Page {path} returned {page.status_code} instead of {status_code}",
    )
    if check_templates:
        self.assertTemplateUsed(page, "base.html", f"Page {path} did not use base.html")
        self.assertTemplateUsed(page, template, f"Page {path} did not use {template}")


def post_page(
    self: TestCase,
    path: str,
    data: dict,
    status_code: int = 200,
):
    """_summary_: Sends a post request to a page and tests the response

    Args:
        self (TestCase): The test case
        path (str): The path to test
        data (dict): The data to send in the post request
        status_code (int, optional): The expected status code. Defaults to 200.
    """
    page = self.client.post(path, data)
    self.assertEqual(
        page.status_code,
        status_code,
        f"Page {path} returned {page.status_code} instead of {status_code}",
    )


# Create a user with garbage data
def createUser(_self: TestCase) -> User:
    """_summary_: Creates a user with garbage data

    Args:
        _self (TestCase): The test case

    Returns:
        User: The user that was created
    """
    user = User.objects.create(
        username="".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10)),
        first_name="".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10)),
        last_name="".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10)),
        email="".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10))
        + "@"
        + "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=10)),
    )
    user.set_password("password")
    user.save()
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


def createCaregiver(_self: TestCase) -> User:
    """_summary_: Creates a caregiver and links it to a user

    Args:
        _self (TestCase): The test case

    Returns:
        User: The user that was created
    """
    user = createUser(_self)
    caregiver = Caregiver.objects.create()
    user.caregiver = caregiver
    user.is_caregiver = True
    user.save()
    return user
