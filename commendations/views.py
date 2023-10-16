from datetime import datetime

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import redirect, render
from django.utils.timezone import make_aware

from commendationSite.authHelper import get_student, role_required
from students.models import Student
from teachers.models import Teacher

from .models import Commendation, Milestone

# Create your views here.


@role_required(teacher=True)
def giveCommendation(request):
    """Award commendations to students."""
    if request.method == "POST":
        commendationType = request.POST["commendationType"]

        # Reason processing
        quickReason = request.POST["quickReason"]
        reason = request.POST["reason"]

        if quickReason == "" and reason == "":
            reason = "No reason given"

        elif quickReason != "" and reason == "":
            reason = quickReason

        elif quickReason != "" and reason != "":
            reason = f"{quickReason}: {reason}"

        rawStudents = request.POST["selectedStudents"]
        # Split the students into a list
        students = rawStudents.split(",")
        # Remove any empty strings, duplicates, convert to ints and remove non-existent students
        students = list(set(filter(lambda student: student != "", students)))
        students = list(map(lambda student: int(student), students))
        students = list(
            filter(lambda student: Student.objects.filter(id=student), students)
        )

        # If no students were selected, return an error
        if len(students) == 0:
            messages.error(request, "No students were selected")
            return redirect("/commendations/award/")

        # Get the teacher that is awarding the commendation
        teacher = Teacher.objects.get(id=request.POST["teacher"])

        # Create a new commendation for the student(s)
        commendation = Commendation(
            teacher=teacher,
            reason=reason,
            commendation_type=commendationType,
        )
        # Must save the commendation before adding students
        commendation.save()

        # Add the students to the commendation
        for student in students:
            student = Student.objects.get(id=student)
            commendation.students.add(student)

        # Save the commendation
        commendation.save()

        # Check each student for a milestone
        for student in students:
            student = Student.objects.get(id=student)
            for milestoneType in Milestone.MILESTONE_TYPE_CHOICES:
                # Get the int value of the milestone type
                milestoneValue = milestoneType[0]
                # Check if the student has now met the milestone number of commendations
                if student.commendation_set.count() == milestoneValue:
                    # Create a milestone for the student
                    milestone = Milestone(
                        student=student, milestone_type=milestoneValue
                    )
                    milestone.save()

                    # Inform the teacher that the student has met the milestone
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        f"{student} has enough commendations to reach a {milestoneType[1]}! This will be awarded automatically.",
                    )

        # Message the user
        messages.add_message(
            request,
            messages.SUCCESS,
            f"Commendation awarded to {len(students)} students!",
        )

        return redirect("/commendations/award/")

    # Process and render the award commendation page
    _commendationTypes = []
    _commendationLocations = []

    for Type in Commendation.COMMENDATION_TYPE_CHOICES:
        _commendationTypes.append({"name": Type[1], "value": Type[0]})
    for Location in Commendation.INSIDE_OUTSIDE_CHOICES:
        _commendationLocations.append({"name": Location[1], "value": Location[0]})

    # If there is a teacher signed in, then the only teacher that should show is themselves
    teachers = Teacher.objects.filter(user=request.user)

    # Filter students to year 9 and 10 only
    students = Student.objects.filter(year_level__in=[9, 10])

    # Generate context and render the page
    context = {
        "commendationTypes": _commendationTypes,
        "commendationLocations": _commendationLocations,
        "students": students,
        "teachers": teachers,
    }

    return render(request, "commendations/award.html", context)


@role_required(teacher=True, management=True)
def awardMilestones(request):
    """The page where teachers can award milestones"""
    if request.method == "POST":
        # there will be a list of milestone IDs
        milestoneIDs = request.POST.getlist("milestone")

        # Get the milestone objects
        milestones = Milestone.objects.filter(id__in=milestoneIDs)

        # Remove any that have already been awarded
        milestones = milestones.filter(awarded=False)
        # If milestones were removed for being awarded, inform the user
        if len(milestones) != len(milestoneIDs):
            messages.warning(
                request,
                "Some milestones have not been changed as they were already marked as awarded",
            )

        # If there are no milestones
        if len(milestones) == 0:
            messages.warning(
                request, "No milestones were awarded as no valid ones were selected"
            )
            return redirect("/commendations/spirit/")

        # Mark the milestones as awarded
        for milestone in milestones:
            milestone.awarded = True
            milestone.save()

        messages.success(request, f"Marked {len(milestones)} milestones as awarded")
        return redirect("/teachers/")

    # Get all milestones
    milestoneTypes = Milestone.MILESTONE_TYPE_CHOICES
    milestones = Milestone.objects.all()

    # Filter dates
    dateQuery = request.GET.get("date")
    if dateQuery:
        # Convert the date to a datetime object
        date = make_aware(datetime.strptime(dateQuery, "%Y-%m-%d"))
        milestones = milestones.filter(date_time__gte=date)

    # Filter by type
    milestoneTypeQuery = request.GET.getlist("type")
    if milestoneTypeQuery:
        milestones = milestones.filter(milestone_type__in=milestoneTypeQuery)

    # Sort by the type then by student name
    milestones = milestones.order_by(
        "awarded",
        "milestone_type",
        "student__user__first_name",
        "student__user__last_name",
    )

    # Untupple the milestone types
    milestoneTypes = [
        {"value": milestoneType[0], "name": milestoneType[1]}
        for milestoneType in milestoneTypes
    ]

    # If no filters are applied, return no milestones
    if not milestoneTypeQuery and not dateQuery:
        milestones = []

    # return the page
    return render(
        request,
        "commendations/award_milestones.html",
        {"milestones": milestones, "milestoneTypes": milestoneTypes},
    )


@role_required(student=True, caregiver=True)
@get_student()
def myCommendations(request, student: Student = None):
    commendations = student.commendation_set.all().order_by("-date_time")
    commendationsSinceLastLogin = commendations.filter(
        date_time__gte=request.user.previous_login or request.user.last_login
    )

    return render(
        request,
        "commendations/my_commendations.html",
        {
            "commendations": commendations,
            "studentSwitcherEnabled": True,
            "commendationsSince": commendationsSinceLastLogin,
            "student": student,
        },
    )


@role_required(student=True, caregiver=True)
@get_student()
def commendationDetail(request, commendation_id, student: Student = None):
    """The page where students can view the details of a commendation"""
    try:
        commendation = Commendation.objects.get(id=commendation_id)
    except Commendation.DoesNotExist:
        raise Http404("Commendation does not exist")

    # Check if the student is in the commendation
    if student not in commendation.students.all():
        raise PermissionDenied

    return render(
        request,
        "commendations/detailed_commendation.html",
        {
            "commendation": commendation,
            "student": student,
        },
    )


@role_required(student=True, caregiver=True)
@get_student()
def milestoneProgress(request, student: Student = None):
    """The page where students can view their progress towards milestones"""
    milestones = Milestone.objects.filter(student=student).order_by("-milestone_type")
    commendations = student.commendation_set.all().order_by("-date_time")
    # For each milestone type, calculate the progress as a percentage
    progress = []
    for milestoneType in Milestone.MILESTONE_TYPE_CHOICES:
        # Get the int value of the milestone type
        milestoneValue = milestoneType[0]
        # Get the number of commendations the student has
        commendationCount = commendations.count()
        # Calculate the percentage
        percentage = (commendationCount / milestoneValue) * 100
        # Dont allow the percentage to be over 100
        min(percentage, 100)
        # Add the percentage to the list
        progress.append(
            {
                "type": milestoneType[1],
                "percentage": round(percentage),
                "value": round(milestoneValue),
                "remaining": round(milestoneValue - commendationCount),
            }
        )

    return render(
        request,
        "commendations/milestone_progress.html",
        {
            "milestones": milestones,
            "commendations": commendations,
            "commendationCount": commendationCount,
            "milestoneProgress": progress,
            "student": student,
            "studentSwitcherEnabled": True,
        },
    )
