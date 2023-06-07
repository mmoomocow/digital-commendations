import json

from django.contrib import auth as django_auth
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from . import authentication as ms_auth

# Create your views here.


def login(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method != "POST":
        auth_uri = ms_auth.BACKEND.setup(request)
        return render(request, "users/login.html", {"auth_uri": auth_uri})

    # Triggered if the client has submitted the form
    username = request.POST["username"]
    password = request.POST["password"]
    # Checks if the user is valid
    user = django_auth.authenticate(request, username=username, password=password)
    if user is not None:
        # Restrict access to active teachers for now
        if user.is_active and user.is_teacher:
            django_auth.login(request, user)
            messages.add_message(
                request,
                messages.SUCCESS,
                f"Login successful! Welcome back {user.first_name}",
            )

            # Check for a next parameter in the URL
            if "next" in request.GET:
                return redirect(request.GET["next"])
            return redirect("/")

        # Deny all other users
        raise PermissionDenied("Sorry, you are not permitted to login!")
    # Deny invalid users
    return render(
        request,
        "users/login.html",
        {
            "error": 'Invalid username or password, <a href="/users/forgot/">forgot your password?</a>',
            "username": username,
        },
        status=403,
    )


def callback(request):
    print("Callback")
    user = ms_auth.authenticate(request)
    print(f"Got user {user} from ms_auth.authenticate\n\n\n")

    if user is not None:
        if user.is_active and user.is_teacher:
            ms_auth.BACKEND.login(request, user)
            print("Logged in")

            # Check for a next parameter in the URL
            if "next" in request.GET:
                return redirect(request.GET["next"])
            return redirect("/users/test/")


def logout(request):
    django_auth.logout(request)
    return redirect("/")


def test(request):
    print(f"User authenticated: {request.user.is_authenticated}")
    print(f"User is anonymous: {request.user.is_anonymous}")
    return HttpResponse("Test")
