from django.shortcuts import render
from commendations.models import commendation
from teachers.models import Teacher
from students.models import Student

# Create your views here.


def index(request):
    return render(request, "teachers/index.html")


def giveCommendation(request):
    if request.method == "post":
        commendationType = request.POST["commendationType"]
        reason = request.POST["reason"]
        rawStudents = request.POST.getlist("students")
        students = Student.objects.filter(id__in=rawStudents)
        teacher = Teacher.objects.get(request.POST["teacher"])

        print(commendationType, reason, students, teacher)

        newCommendation = commendation(
            teacher=teacher,
            reason=reason,
            type=commendationType,
        )
        newCommendation.save()

        for student in students:
            newCommendation.students.add(student)

        return render(request, "teachers/index.html")

    _commendationTypes = []

    for Type in commendation.COMMENDATION_TYPE_CHOICES:
        _commendationTypes.append({"name": Type[1], "value": Type[0]})
    students = Student.objects.all()
    teachers = Teacher.objects.all()

    # If there is a teacher signed in, then the only teacher that should show is themselves
    if request.user.is_authenticated:
        teachers = Teacher.objects.filter(user=request.user)

    context = {
        "commendationTypes": _commendationTypes,
        "students": students,
        "teachers": teachers,
    }

    return render(request, "teachers/giveCommendation.html", context)
