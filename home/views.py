from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Contact

# Create your views here.


def index(request) -> render:
    """Direct users to the appropriate page."""
    return render(request, "home/index.html")


@login_required()
def portals(request) -> render:
    """Display the appropriate portal for the user."""
    if request.user.is_teacher:
        return render(request, "home/home_teacher.html")
    if request.user.is_student:
        # Get all commendations since previous login
        commendations = request.user.student.commendation_set.filter(
            date_time__gte=request.user.previous_login or request.user.last_login
        )
        # Message the user if they have new commendations
        if commendations:
            messages.info(
                request,
                f"You have {len(commendations)} new commendation(s)! Follow the link below to view them.",
                extra_tags="commendations",
            )
        return render(request, "home/home_student.html")
    if request.user.is_caregiver:
        return render(request, "home/home_caregiver.html")
    if request.user.is_superuser:
        return redirect("/admin/", permanent=False)
    return redirect("/", permanent=False)


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
