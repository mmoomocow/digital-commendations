from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
	pass

@admin.register(Caregiver)
class CaregiverAdmin(admin.ModelAdmin):
	pass
