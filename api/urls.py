from django.urls import path
from .views import KAMAR_check

urlpatterns = [
    path("check/", KAMAR_check, name="check"),
]
