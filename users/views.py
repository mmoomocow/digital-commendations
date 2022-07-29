from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.


def loginView(request):
    """
    View for the login page.
    GET requests will render the login page.
    POST requests will authenticate the user and redirect them to the home page.
    """
    if request.user.is_authenticated:
        messages.add_message(request, messages.INFO, "You are already logged in!")
        return redirect("/")

    if request.method == "POST":
        # Triggered if the client has submitted the form
        username = request.POST["username"]
        password = request.POST["password"]
        # Checks if the user is valid
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Restrict access to active teachers for now
            if user.is_active:
                if user.is_teacher:
                    login(request, user)
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        f"Login successful! Welcome back {user.first_name}",
                    )
                    return redirect("/")
                return render(
                    request,
                    "users/login.html",
                    {
                        "error": "Sorry, only teachers can log in!",
                        "username": username,
                    },
                    status=403,
                )
            return render(
                request,
                "users/login.html",
                {
                    "error": "You have been marked inactive, so cannot log in.",
                    "username": username,
                },
                status=403,
            )
        return render(
            request,
            "users/login.html",
            {
                "error": 'Invalid username or password, <a href="/users/forgot/">forgot your password?</a>',
                "username": username,
            },
            status=403,
        )

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
        return redirect("/")
    messages.add_message(
        request, messages.INFO, "You are not logged in, so you cannot log out!"
    )
    return redirect("/")
