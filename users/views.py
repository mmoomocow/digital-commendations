from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate as django_authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .backends import MicrosoftAuthBackend

# Create your views here.

ms_backend_path = "users.backends.MicrosoftAuthBackend"


def login(request):
    """Login view."""
    if ms_backend_path not in settings.AUTHENTICATION_BACKENDS:
        raise ImproperlyConfigured(
            f"{ms_backend_path} not in AUTHENTICATION_BACKENDS, please add it."
        )
    ms_auth = MicrosoftAuthBackend()

    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect(settings.LOGIN_REDIRECT_URL)

    if request.method != "POST":
        ms_auth.setup(request)
        return render(
            request, "users/login.html", {"auth_uri": ms_auth.get_auth_uri(request)}
        )

    # Must be a POST request with username and password - attempt to authenticate

    username = request.POST.get("username")
    password = request.POST.get("password")

    user = django_authenticate(
        request,
        username=username,
        password=password,
        backend="django.contrib.auth.backends.ModelBackend",
    )
    if user is not None and user.is_active:
        django_login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        messages.success(request, "You have successfully logged in.")
        return redirect(settings.LOGIN_REDIRECT_URL)
    raise PermissionDenied


def logout(request):
    """Logout view."""

    if not request.user.is_authenticated:
        messages.info(request, "You were not logged in, nothing has changed.")
        return redirect(settings.LOGOUT_REDIRECT_URL)

    django_logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect(settings.LOGOUT_REDIRECT_URL)


def callback(request):
    """Callback for microsoft auth."""
    if ms_backend_path not in settings.AUTHENTICATION_BACKENDS:
        raise ImproperlyConfigured(
            f"{ms_backend_path} not in AUTHENTICATION_BACKENDS, please add it."
        )
    # Reject if not a GET request with a code parameter
    if request.method != "GET" or "code" not in request.GET:
        raise PermissionDenied

    user = django_authenticate(request)
    print(user)
    if user is not None and user.is_active:
        django_login(request, user, backend="users.backends.MicrosoftAuthBackend")
        messages.success(request, "You have successfully logged in.")
        return redirect("/users/test/")
    raise PermissionDenied
