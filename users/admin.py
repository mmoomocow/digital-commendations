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
	filter_horizontal = ('groups', 'user_permissions')
	fieldsets = (
		(None, {
			'fields': ('username', 'password', 'last_login', 'id')
		}),
		('Personal info', {
			'fields': ('first_name', 'last_name', 'email', 'title')
		}),
		('Permissions', {
			'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
		}),
		('User Links', {
			'fields': ('is_teacher', 'is_student', 'is_caregiver', 'teacher', 'student', 'caregiver')
		}),
	)

	def delete_model(self, request, obj):
		for user in obj.all():
			if user.is_superuser:
				return False
			else:
				super().delete_model(request, obj)
