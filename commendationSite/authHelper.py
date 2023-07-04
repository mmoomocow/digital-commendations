from typing import Optional

from django.core.exceptions import PermissionDenied

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
