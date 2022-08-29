from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("students/<int:ID>/", views.student, name="students"),
    path("students/", views.students, name="student"),
    path("badges/", views.awardMilestones, name="badges"),
]
