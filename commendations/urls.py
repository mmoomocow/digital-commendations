from django.urls import path

from . import views

urlpatterns = [
    path("award/", views.giveCommendation, name="giveCommendation"),
    path("spirit/", views.awardMilestones, name="viewMilestones"),
    path("my/", views.myCommendations, name="myCommendations"),
    path(
        "detail/<int:commendation_id>/",
        views.commendationDetail,
        name="commendationDetail",
    ),
    path("progress/", views.milestoneProgress, name="milestoneProgress"),
]
