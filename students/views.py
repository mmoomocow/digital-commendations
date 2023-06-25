from django.db.models import Q
from django.http import Http404
from django.shortcuts import render

from commendationSite.authHelper import role_required

from .models import Student

# Create your views here.


@role_required(teacher=True, management=True)
def listStudents(request):
    """The page where teachers can see students"""
    studentList = Student.objects.all()

    # If there is a search query, filter the students
    if request.GET.get("search"):
        # Search user.first_name, user.last_name, user.email, user.username, id
        studentList = studentList.filter(
            Q(user__first_name__icontains=request.GET.get("search"))
            | Q(user__last_name__icontains=request.GET.get("search"))
            | Q(user__email__icontains=request.GET.get("search"))
            | Q(user__username__icontains=request.GET.get("search"))
            | Q(id__icontains=request.GET.get("search"))
        )

    # Sort the students by first name
    studentList = studentList.order_by("user__first_name", "user__last_name")

    # Return the page
    return render(
        request,
        "students/list_students.html",
        {"students": studentList, "query": request.GET.get("search")},
    )


@role_required(teacher=True, management=True)
def studentInfo(request, ID: int = None):
    """The page where teachers can see students"""
    # Get the student
    try:
        selectedStudent = Student.objects.get(id=ID)
    # If the student does not exist, return a 404
    except Student.DoesNotExist:
        raise Http404("Student does not exist")

    # Commendations that the student has received
    commendations = selectedStudent.commendation_set.all().order_by("-date_time")
    milestones = selectedStudent.milestone_set.all().order_by("-date_time")

    return render(
        request,
        "students/student_info.html",
        {
            "student": selectedStudent,
            "commendations": commendations,
            "milestones": milestones,
        },
    )
