# Custom error views
from django.shortcuts import redirect, render


def error_404(request, exception):
    """Custom 404 error view."""
    return render(request, "errors/404.html")
