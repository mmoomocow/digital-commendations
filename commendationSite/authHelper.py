from typing import Optional

from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from students.models import Student
from users.models import User


def role_required(
    student: Optional[bool] = False,
    teacher: Optional[bool] = False,
    management: Optional[bool] = False,
    caregiver: Optional[bool] = False,
    staff: Optional[bool] = False,
    superuser: Optional[bool] = True,
):
    """Checks if the user is logged in as a teacher and optionally if they are management

    Args:
        student (Optional[bool], optional): Whether the user must be a student. Defaults to False.
        teacher (Optional[bool], optional): Whether the user must be a teacher. Defaults to False.
        management (Optional[bool], optional): Whether the user must be management. Defaults to False.
        caregiver (Optional[bool], optional): Whether the user must be a caregiver. Defaults to False.
        staff (Optional[bool], optional): Whether the user must be staff. Defaults to False.
        superuser (Optional[bool], optional): Whether the user must be a superuser. Defaults to True.
    """

    def decorator(view):
        """The decorator that wraps the view"""

        def inner(request, *args, **kwargs):
            """The inner function that checks if the user is a teacher"""
            # Check if the user is logged in
            if not request.user.is_authenticated:
                raise PermissionDenied

            # If the user is any of the roles, allow the view
            # If there are multiple roles, allow the view if the user is any of them
            if (
                (student and request.user.is_student)
                or (teacher and request.user.is_teacher)
                or (management and request.user.is_teacher)
                or (caregiver and request.user.is_caregiver)
                or (staff and request.user.is_staff)
                or (superuser and request.user.is_superuser)
            ):
                if management and request.user.teacher is not None:
                    # Nested if statement to prevent errors if the user is not a teacher
                    if not request.user.teacher.is_management:
                        raise PermissionDenied

                # Return the view
                return view(request, *args, **kwargs)

            # If the user is not any of the roles, deny the view
            raise PermissionDenied

        return inner

    return decorator


def get_student():
    """Gets the current student, if they are a student or a caregiver of a student"""

    def decorator(view):
        """The decorator that wraps the view"""

        def inner(request, *args, **kwargs):
            """The inner function that gets the student"""

            # Return if not logged in
            if not request.user.is_authenticated:
                return

            if request.user.is_student:
                # If the user is a student, return the student
                kwargs["student"] = request.user.student
                return view(request, *args, **kwargs)

            if not request.user.is_caregiver:
                # If the user is not a caregiver, return
                return

            if "viewAs" not in request.session:
                # Set the viewAs session variable to the first student
                request.session["viewAs"] = request.user.caregiver.students.first().id

            try:
                # Try to get the student from the session
                student = Student.objects.get(id=request.session["viewAs"])
            except User.DoesNotExist:
                # If the student does not exist, return the student switcher
                request.session["viewAs"] = request.user.caregiver.students.first().id

            # If the user is a caregiver of the student, allow the view
            if student in request.user.caregiver.students.all():
                kwargs["student"] = student
                return view(request, *args, **kwargs)

            # If the user is not a caregiver of the student, deny the view
            raise PermissionDenied

        return inner

    return decorator


def can_login(user: User) -> bool:
    """Checks if the user can login

    Args:
        user (User): The user to check

    Returns:
        bool: Whether the user can login or not
    """
    return (
        user.is_active
        and (
            user.is_teacher or user.is_student or user.is_caregiver or user.is_superuser
        )
        and not user.is_anonymous
    )
