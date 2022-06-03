from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(commendation)
class CommendationAdmin(admin.ModelAdmin):
	list_display = ('id', 'commendation_type', 'date_time', 'teacher')
	list_filter = ('commendation_type', 'date_time', 'teacher')
	search_fields = ('id', 'commendation_type', 'date_time', 'teacher', 'reason', 'students')
	readonly_fields = ('id', 'date_time')
	filter_horizontal = ('students',)
	fieldsets = (
		(None, {
			'fields': ('id',)
		}),
		('Commendation', {
			'fields': ('commendation_type', 'reason', 'date_time')
		}),
		('User Links', {
			'fields': ('teacher', 'students')
		}),
	)
