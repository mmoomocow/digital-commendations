from django.urls import path

from . import views

urlpatterns = [
    path("<int:ID>/", views.studentInfo, name="students"),
    path("", views.listStudents, name="student"),
]
