from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'tutor_room', 'house_group', 'year_level',)
	list_filter = ('house_group', 'year_level',)
	search_fields = ('id', 'user__first_name', 'user__last_name')

@admin.register(Caregiver)
class CaregiverAdmin(admin.ModelAdmin):
	pass
