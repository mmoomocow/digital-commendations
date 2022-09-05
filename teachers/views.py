from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from commendations.models import Milestone


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


def awardMilestones(request):
    """The page where teachers can award milestones"""
    # Check if user is logged in
    if not request.user.is_authenticated:
        # messages.error(request, "You must be logged in to award milestones")
        return HttpResponse(status=403)
    # Check if user is a teacher
    if not request.user.is_teacher:
        # messages.error(request, "You must be a teacher to award milestones")
        return HttpResponse(status=403)
    if not request.user.teacher.is_management:
        # messages.error(request, "You must be a management teacher to award milestones")
        return HttpResponse(status=403)

    if request.method == "POST":
        # there will be a list of milestone IDs
        milestoneIDs = request.POST.getlist("milestone")

        # Check that the milestones exist
        milestones = Milestone.objects.filter(id__in=milestoneIDs)
        if len(milestones) == 0:
            # messages.error(request, "Those milestones do not exist")
            return HttpResponse(status=404)
        # Check that the milestones are not already awarded
        milestones = milestones.filter(awarded=False)
        if len(milestones) == 0:
            # messages.error(request, "Those milestones have already been awarded")
            return HttpResponse(status=400)

        # Mark the milestones as awarded
        for milestone in milestones:
            milestone.awarded = True
            milestone.save()

        messages.success(request, f"Marked {len(milestones)} milestones as awarded")
        return redirect("/teachers/")

    milestoneTypes = Milestone.MILESTONE_TYPE_CHOICES
    milestones = Milestone.objects.all()

    milestoneTypeQuery = request.GET.getlist("type")
    if milestoneTypeQuery:
        milestones = milestones.filter(milestone_type__in=milestoneTypeQuery)

    dateQuery = request.GET.get("date")
    if dateQuery:
        milestones = milestones.filter(date_time__gte=dateQuery)

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

    return render(
        request,
        "teachers/award_milestones.html",
        {"milestones": milestones, "milestoneTypes": milestoneTypes},
    )
