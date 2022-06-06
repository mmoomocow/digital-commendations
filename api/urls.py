from django.urls import path
from .views import *

urlpatterns = [
	path('check/', KAMAR_check, name='check'),
]
