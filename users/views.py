from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def loginView(request):
    if request.user.is_authenticated:
        # Don't allow logged in users to login again
        return render(
            request,
            "users/login.html",
            {
                "success": True,
                "error": f'<p style="color:green;">Already logged in. Welcome {request.user.first_name}</p>',
            },
            status=202,
        )

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
                    return render(
                        request,
                        "users/login.html",
                        {
                            "success": True,
                            "error": f'<p style="color:green;">Login successful. Welcome {user.first_name}</p>',
                        },
                        status=202,
                    )
                else:
                    return render(
                        request,
                        "users/login.html",
                        {
                            "error": "Sorry, only teachers can log in!",
                            "username": username,
                        },
                        status=403,
                    )
            else:
                return render(
                    request,
                    "users/login.html",
                    {
                        "error": "You have been marked inactive, so cannot log in.",
                        "username": username,
                    },
                    status=403,
                )
        else:
            return render(
                request,
                "users/login.html",
                {
                    "error": 'Invalid username or password, <a href="/users/forgot/">forgot your password?</a>',
                    "username": username,
                },
                status=403,
            )

    else:
        # Triggered if the client has not filled out the form, so send them the login page
        return render(request, "users/login.html")


def logoutView(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponse(
            "<h1>Logout successful</h1>"
        )  # Basic HTTP more work on front end will be done later
    else:
        return HttpResponse("<h1>You are not logged in</h1>")
