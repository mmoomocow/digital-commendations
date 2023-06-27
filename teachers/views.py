from django.shortcuts import render

from commendationSite.authHelper import role_required

# Create your views here.


@role_required(teacher=True)
def index(request):
    """The index page for teachers."""
    return render(request, "teachers/index.html")
