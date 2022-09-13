from django.shortcuts import HttpResponse


def teacher_required(is_management: bool = False):
    """Checks if the user is logged in as a teacher and optionally if they are management

    Args:
        is_management (bool, optional): If true the teacher must be management to view the page. Defaults to False.
    """

    def decorator(view):
        """The decorator that wraps the view"""

        def inner(request, *args, **kwargs):
            """The inner function that checks if the user is a teacher"""
            # Check if the user is logged in
            if not request.user.is_authenticated:
                return HttpResponse(status=401)

            # Check if the user is a teacher
            if not request.user.is_teacher:
                return HttpResponse(status=403)

            # Check if the user is management
            if is_management and not request.user.teacher.is_management:
                return HttpResponse(status=403)

            # If all checks pass, run the view
            return view(request, *args, **kwargs)

        return inner

    return decorator