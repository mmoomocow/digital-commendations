"""commendationSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

urlpatterns = [
    path("api/", include("api.urls")),
    path("login/", RedirectView.as_view(url="/users/login/", permanent=True)),
    path("logout/", RedirectView.as_view(url="/users/logout/", permanent=True)),
    path("users/", include("users.urls")),
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
    path("teachers/", include("teachers.urls")),
    path("commendations/", include("commendations.urls")),
    path("students/", include("students.urls")),
    path("", include("home.urls")),
]

# Set admin site titles
admin.site.site_header = "Bayfield Commendations Administration"
admin.site.site_title = "Bayfield Commendations Admin Portal"
admin.site.index_title = "Welcome to Bayfield's Commendation Site Admin Portal"

# Custom error views
handler403 = "home.views_errors.error_403"
handler404 = "home.views_errors.error_404"
handler500 = "home.views_errors.error_500"
