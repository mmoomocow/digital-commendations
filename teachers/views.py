from django.shortcuts import render

from commendationSite.authHelper import teacher_required

# Create your views here.


@teacher_required()
def index(request):
    """The index page for teachers."""
    return render(request, "teachers/index.html")
