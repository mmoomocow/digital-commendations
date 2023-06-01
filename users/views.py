from django.contrib import auth as django_auth
from django.contrib import messages
from django.shortcuts import redirect, render

from .authentication import BACKEND, BACKEND_PATH, authenticate

# Create your views here.


def login(request):
    if request.method != "POST":
        auth_uri = BACKEND.setup(request)
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
        return render(
            request,
            "users/login.html",
            {
                "error": "Sorry, you are not permitted to login!",
                "username": username,
            },
            status=403,
        )
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
    user = authenticate(request)
    if user is not None:
        django_auth.login(request, user, backend=BACKEND_PATH)
        messages.add_message(
            request,
            messages.SUCCESS,
            f"Login successful! Welcome back {user.first_name}",
        )

        # Check for a next parameter in the URL
        if "next" in request.GET:
            return redirect(request.GET["next"])
        return redirect("/")
    return redirect("/")


def logout(request):
    django_auth.logout(request)
    return redirect("/")
