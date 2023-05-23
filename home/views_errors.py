# Custom error views
from django.shortcuts import render


def error_403(request, exception):
    """Custom 403 error view."""
    return render(
        request, "errors/403.html", context={"request": request, "exception": exception}
    )


def error_404(request, exception):
    """Custom 404 error view."""
    return render(
        request, "errors/404.html", context={"request": request, "exception": exception}
    )


def error_500(request, exception):
    """Custom 500 error view."""
    return render(
        request, "errors/500.html", context={"request": request, "exception": exception}
    )
