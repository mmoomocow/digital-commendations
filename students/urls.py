from django.urls import path
from . import views


urlpatterns = [
    path("<int:ID>/", views.student, name="students"),
    path("", views.students, name="student"),
]
