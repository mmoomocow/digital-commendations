# Custom error views
from django.shortcuts import redirect, render


def error_403(request, exception):
    """Custom 403 error view."""
    return render(
        request, "errors/403.html", context={"request": request, "exception": exception}
    )


def error_404(request, exception):
    """Custom 404 error view."""
    # If there is no trailing slash, redirect to the same URL with a trailing slash
    if not request.path.endswith("/"):
        print("Missing trailing slash; redirecting to " + request.path + "/")
        return redirect(request.path + "/", permanent=True)
    return render(
        request, "errors/404.html", context={"request": request, "exception": exception}
    )


def error_500(request):
    """Custom 500 error view."""
    return render(request, "errors/500.html", context={"request": request})
