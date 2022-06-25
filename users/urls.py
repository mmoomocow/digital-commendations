from django.urls import path
from .views import loginView, logoutView

urlpatterns = [
    path("login/", loginView, name="login"),
    path("logout/", logoutView, name="logout"),
]
