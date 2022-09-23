from django.shortcuts import render
from .models import Contact

# Create your views here.


def index(request) -> render:
    """The home page of the website."""
    return render(request, "home/index.html")


def contact(request) -> render:
    """The contact page of the website."""
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        newContact = Contact(name=name, email=email, subject=subject, message=message)
        newContact.save()

        return render(request, "home/contacted.html", status=201)
    return render(request, "home/contact.html")
