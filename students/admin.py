from django.contrib import admin

from .models import Caregiver, Student

# Register your models here.


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Admin settings for the student model."""

    list_display = (
        "id",
        "user",
        "tutor_room",
        "house_group",
        "year_level",
    )
    list_filter = (
        "house_group",
        "year_level",
    )
    search_fields = ("id", "user__first_name", "user__last_name")
    ordering = ("id", "user__first_name", "user__last_name")


@admin.register(Caregiver)
class CaregiverAdmin(admin.ModelAdmin):
    """Admin settings for the caregiver model."""

    list_display = (
        "id",
        "user",
        "list_students",
    )

    search_fields = ("id", "user__first_name", "user__last_name")

    ordering = ("id", "user__first_name", "user__last_name")

    list_students = lambda _, obj: ", ".join(
        [str(s) for s in obj.students.all().order_by("id")]
    )
    list_students.short_description = "Students"
