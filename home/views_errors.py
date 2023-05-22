# Custom error views
from django.shortcuts import redirect, render


def error_403(request, exception):
    """Custom 403 error view."""
    return render(request, "errors/403.html")


def error_404(request, exception):
    """Custom 404 error view."""
    return render(request, "errors/404.html")


def error_500(request):
    """Custom 500 error view."""
    return render(request, "errors/500.html")
