# Custom error views
from django.conf import settings
from django.shortcuts import redirect, render


def error_403(request, exception):
    """Custom 403 error view."""
    return render(
        request, "errors/403.html", context={"request": request, "exception": exception}
    )


def error_404(request, exception):
    """Custom 404 error view."""
    # If there is no trailing slash, redirect to the same URL with a trailing slash
    # See https://github.com/mmoomocow/digital-commendations/issues/153
    APPEND_SLASH = getattr(settings, "APPEND_SLASH", True)
    if not request.path.endswith("/") and APPEND_SLASH:
        return redirect(request.path + "/", permanent=True)

    return render(
        request, "errors/404.html", context={"request": request, "exception": exception}
    )


def error_500(request):
    """Custom 500 error view."""
    return render(request, "errors/500.html", context={"request": request})
