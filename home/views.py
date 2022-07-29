from django.shortcuts import render

# Create your views here.


def index(request) -> render:
    """The home page of the website."""
    return render(request, "home/index.html")
