from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages

# Create your views here.


def index(request):
    """The index page for teachers."""
    # Check if user is logged in
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to give a commendation.")
        return HttpResponse(status=403)
    # Check if user is a teacher
    if not request.user.is_teacher:
        messages.error(request, "You must be a teacher to give a commendation.")
        return HttpResponse(status=403)

    return render(request, "teachers/index.html")
