from django.contrib import admin
from .models import Contact

# Register your models here.


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Admin settings for the contact model."""

    list_display = ("name", "email", "subject", "message", "status")
    fieldsets = (
        (None, {"fields": ("name", "email", "subject", "message")}),
        ("Status", {"fields": ("status",)}),
    )
    readonly_fields = ("name", "email", "subject", "message")
    list_filter = ("status",)
    search_fields = ("name", "email", "subject", "message")

    # Mark the message as replied
    def mark_as_replied(self, request, queryset):
        """Mark the message as replied."""
        queryset.update(status=Contact.REPLIED)

    # Mark the message as done
    def mark_as_done(self, request, queryset):
        """Mark the message as done."""
        queryset.update(status=Contact.DONE)

    # Mark the message as not replied
    def mark_as_not_replied(self, request, queryset):
        """Mark the message as not replied."""
        queryset.update(status=Contact.NOT_REPLIED)

    # Add the actions to the admin page
    actions = [mark_as_replied, mark_as_done, mark_as_not_replied]
