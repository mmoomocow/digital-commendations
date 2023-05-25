from django.contrib import admin

from .models import Teacher

# Register your models here.


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    """Admin settings for the teacher model."""

    list_display = (
        "staff_code",
        "user",
        "house_group",
    )
    list_filter = ("house_group",)
    search_fields = ("staff_code", "user__first_name", "user__last_name")
    ordering = ("staff_code",)
