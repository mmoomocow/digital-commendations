from django.contrib import admin

from .models import Commendation, Milestone

# Register your models here.


@admin.register(Commendation)
class CommendationAdmin(admin.ModelAdmin):
    """Admin settings for the commendation model."""

    list_display = ("id", "commendation_type", "date_time", "teacher", "students")
    list_filter = ("commendation_type", "date_time", "teacher")
    search_fields = (
        "id",
        "commendation_type",
        "date_time",
        "teacher",
        "reason",
        "students",
    )
    readonly_fields = ("id", "date_time")
    filter_horizontal = ("students",)
    fieldsets = (
        (None, {"fields": ("id",)}),
        ("Commendation", {"fields": ("commendation_type", "reason", "date_time")}),
        ("User Links", {"fields": ("teacher", "students")}),
    )

    def students(self, obj) -> str:
        """Return a string of the students in the commendation."""
        return ", ".join([str(student) for student in obj.students.all()])


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    """Admin settings for the milestone model."""

    list_display = ("milestone_type", "student", "date_time", "awarded")
    list_filter = ("milestone_type", "date_time", "awarded")
    search_fields = ("milestone_type", "date_time", "reason", "student")
    readonly_fields = ("id", "date_time")
    fieldsets = (
        (None, {"fields": ("id",)}),
        ("Milestone", {"fields": ("milestone_type", "date_time", "awarded")}),
        ("User Links", {"fields": ("student",)}),
    )
