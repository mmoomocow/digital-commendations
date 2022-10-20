from django.shortcuts import redirect, render
from .models import Contact

# Create your views here.


def index(request) -> render:
    """Direct users to the appropriate page.

    If the user is a teacher, they are directed to the award commendation page
    If the user is a superuser, they are directed to the admin page
    Otherwise, they are directed to the home page
    """
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect("/commendations/award/")
        if request.user.is_superuser:
            return redirect("/admin/")
    return redirect("/home/")


def home(request) -> render:
    """The home page of the website."""
    return render(request, "home/index.html")


def about(request) -> render:
    """The about page of the website."""
    return render(request, "home/about.html")


def privacy(request) -> render:
    """The privacy page of the website."""
    return render(request, "home/privacy.html")


def contact(request) -> render:
    """The contact page of the website."""
    # If the user has submitted the form
    if request.method == "POST":
        # Get form data
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        # Create a contact object
        newContact = Contact(name=name, email=email, subject=subject, message=message)
        newContact.save()

        # Message the user
        return render(request, "home/contacted.html", status=201)
    # If the user has not submitted the form
    return render(request, "home/contact.html")
