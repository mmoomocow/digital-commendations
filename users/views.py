from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate as django_authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.shortcuts import redirect, render

from .backends import MicrosoftAuthBackend

# Create your views here.


def login(request):
    """Login view."""

    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect(settings.LOGIN_REDIRECT_URL)

    if request.method != "POST":
        auth_uri = MicrosoftAuthBackend().get_auth_uri(request)
        return render(request, "users/login.html", {"auth_uri": auth_uri})

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

    return render(request, "users/login.html")


def logoutView(request):
    """
    View for the logout page.
    Requests will log the user out and redirect them to the home page.
    """
    if request.user.is_authenticated:
        logout(request)
        messages.add_message(
            request, messages.SUCCESS, "You have been logged out, see you next time!"
        )
        if "next" in request.GET:
            return redirect(request.GET["next"])
        return redirect("/")

    messages.add_message(request, messages.INFO, "You are not logged in!")
    return redirect("/")
