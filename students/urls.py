from django.urls import path

from . import views

urlpatterns = [
    path("list/<int:ID>/", views.studentInfo, name="students"),
    path("list/", views.listStudents, name="student"),
]
