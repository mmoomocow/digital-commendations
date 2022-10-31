from datetime import datetime
from django.shortcuts import redirect, render
from django.contrib import messages
from django.utils.timezone import make_aware
from .models import Commendation, Milestone
from teachers.models import Teacher
from students.models import Student
from commendationSite.authHelper import teacher_required

# Create your views here.


@teacher_required()
def giveCommendation(request):
    """Award commendations to students."""
    if request.method == "POST":
        commendationType = request.POST["commendationType"]
        reason = request.POST["reason"]
        rawStudents = request.POST.getlist("students")
        # rawStudents starts with an empty list, so we need to remove the empty string that is the first element and any non number items and append valid IDs to a new list
        students = []
        for student in rawStudents:
            try:
                students.append(int(student))
            except ValueError:
                pass

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

    for Type in Commendation.COMMENDATION_TYPE_CHOICES:
        _commendationTypes.append({"name": Type[1], "value": Type[0]})
    students = Student.objects.all()
    teachers = Teacher.objects.all()

    # If there is a teacher signed in, then the only teacher that should show is themselves
    teachers = Teacher.objects.filter(user=request.user)

    # Generate context and render the page
    context = {
        "commendationTypes": _commendationTypes,
        "students": students,
        "teachers": teachers,
    }

    return render(request, "commendations/award.html", context)


@teacher_required(is_management=True)
def viewMilestones(request):
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
