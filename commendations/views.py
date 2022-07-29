from django.shortcuts import redirect, render
from django.contrib import messages
from .models import commendation as Commendation
from teachers.models import Teacher
from students.models import Student

# Create your views here.


def giveCommendation(request):
    if request.method == "POST":
        commendationType = request.POST["commendationType"]
        reason = request.POST["reason"]
        rawStudents = request.POST.getlist("students")
        # rawStudents starts with an empty list, so we need to remove the empty string that is the first element
        students = [int(student) for student in rawStudents if student != ""]
        teacher = Teacher.objects.get(id=request.POST["teacher"])

        commendation = Commendation(
            teacher=teacher,
            reason=reason,
            commendation_type=commendationType,
        )
        commendation.save()

        for student in students:
            student = Student.objects.get(id=student)
            commendation.students.add(student)

        commendation.save()

        # Message the user
        messages.add_message(
            request,
            messages.SUCCESS,
            f"Commendation awarded to {len(students)} students!",
        )

        return redirect("/teachers/")

    _commendationTypes = []

    for Type in Commendation.COMMENDATION_TYPE_CHOICES:
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

    return render(request, "commendations/award.html", context)
