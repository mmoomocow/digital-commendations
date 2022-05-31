from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ('username', 'first_name', 'last_name', 'email', 'is_teacher', 'is_student', 'is_caregiver')
	list_filter = ('is_teacher', 'is_student', 'is_caregiver', 'is_staff', 'is_superuser', 'is_active')
	search_fields = ('username', 'email', 'first_name', 'last_name')
	ordering = ('first_name', 'last_name')
	readonly_fields = ('last_login', 'id')
