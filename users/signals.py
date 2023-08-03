from django.utils import timezone

from .models import User


def update_last_visit(sender, **kwargs):  # skipcq: PYL-W0613
    """Update the last viewed time."""
    user: User = kwargs["user"]
    user.previous_login = user.recent_login
    user.recent_login = timezone.now()
    user.save()
