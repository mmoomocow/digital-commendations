from django.urls import path
from . import views


urlpatterns = [
    path("award/", views.giveCommendation, name="giveCommendation"),
    path("spirit/", views.viewMilestones, name="viewMilestones"),
]
