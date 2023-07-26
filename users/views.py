from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate as django_authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect, render

from commendationSite.authHelper import can_login

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

    if not username or not password:
        messages.error(request, "Please enter both username and password.")
        return redirect(settings.LOGIN_URL)
    user = django_authenticate(request, username=username, password=password)
    if user is None:
        messages.error(
            request,
            "We couldn't find your account, are you sure you entered he correct username and password?",
        )
        return redirect(settings.LOGIN_URL)

    if can_login(user):
        django_login(request, user)
        messages.success(
            request, f"You have successfully logged in. Welcome back {user.first_name}!"
        )
        if request.user.is_teacher:
            messages.info(
                request,
                "You will be redirected to the commendation awarding page. To go to the portal, select the portal button from the teacher dropdown above.",
            )
            return redirect("/commendations/award/")
        return redirect(settings.LOGIN_REDIRECT_URL)
    messages.error(
        request,
        "You do not have permission to login. If you believe this is an error, please contact support.",
    )
    return redirect(settings.LOGIN_URL)


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
        messages.error(request, "No code was provided in the request.")
        return redirect(settings.LOGIN_URL)

    user = django_authenticate(request)
    if user is None:
        messages.error(
            request,
            "We couldn't find your account in our system. Please contact support if you believe this unexpected.",
        )
        return redirect(settings.LOGIN_URL)

    if can_login(user):
        django_login(request, user, backend=ms_backend_path)
        messages.success(
            request, f"You have successfully logged in. Welcome back {user.first_name}!"
        )
        if request.user.is_teacher:
            messages.info(
                request,
                "You have been redirected to the award commendation page. To go to the teacher portal, select the portal button from the teacher dropdown below.",
            )
            return redirect("/commendations/award/")
    messages.error(
        request,
        "You do not have permission to login. If you believe this is an error, please contact support.",
    )
    return redirect(settings.LOGIN_URL)
