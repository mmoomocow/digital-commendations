from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse
from students.models import Student


# Create your views here.


def index(request):
    """The index page for teachers."""
    # Check if user is logged in
    if not request.user.is_authenticated:
        # messages.error(request, "You must be logged in to give a commendation.")
        return HttpResponse(status=403)
    # Check if user is a teacher
    if not request.user.is_teacher:
        # messages.error(request, "You must be a teacher to give a commendation.")
        return HttpResponse(status=403)

    return render(request, "teachers/index.html")


def students(request):
    """The page where teachers can see students"""
    # Check if user is logged in
    if not request.user.is_authenticated:
        # messages.error(request, "You must be logged in to view students")
        return HttpResponse(status=403)
    # Check if user is a teacher
    if not request.user.is_teacher:
        # messages.error(request, "You must be a teacher to view students")
        return HttpResponse(status=403)
    if not request.user.teacher.is_management:
        # messages.error(request, "You must be a management teacher to view students")
        return HttpResponse(status=403)

    students = Student.objects.all()

    # If there is a search query, filter the students
    if request.GET.get("search"):
        # Search user.first_name, user.last_name, user.email, user.username, id
        students = students.filter(
            Q(user__first_name__icontains=request.GET.get("search"))
            | Q(user__last_name__icontains=request.GET.get("search"))
            | Q(user__email__icontains=request.GET.get("search"))
            | Q(user__username__icontains=request.GET.get("search"))
            | Q(id__icontains=request.GET.get("search"))
        )

    # Sort the students by first name
    students = students.order_by("user__first_name", "user__last_name")

    # If there is no id, return all students
    return render(
        request,
        "teachers/students.html",
        {"students": students, "query": request.GET.get("search")},
    )


def student(request, ID: int = None):
    """The page where teachers can see students"""
    # Check if user is logged in
    if not request.user.is_authenticated:
        # messages.error(request, "You must be logged in to view students")
        return HttpResponse(status=403)
    # Check if user is a teacher
    if not request.user.is_teacher:
        # messages.error(request, "You must be a teacher to view students")
        return HttpResponse(status=403)
    if not request.user.teacher.is_management:
        # messages.error(request, "You must be a management teacher to view students")
        return HttpResponse(status=403)
    try:
        selectedStudent = Student.objects.get(id=ID)
    except Student.DoesNotExist:
        return HttpResponse(status=404)

    # Commendations that the student has received
    commendations = selectedStudent.commendation_set.all()

    return render(
        request,
        "teachers/student.html",
        {"student": selectedStudent, "commendations": commendations},
    )
