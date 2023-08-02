from django.utils import timezone

from .models import User


def update_last_visit(sender, **kwargs):
    """Update the last viewed time."""
    print("TRIGGERED LOGIN SIGNAL")
    user: User = kwargs["user"]
    print(f"User: {user}")
    user.previous_login = user.recent_login
    print(f"Previous login: {user.previous_login}")
    user.recent_login = timezone.now()
    print(f"Recent login: {user.recent_login}")
    user.save()
