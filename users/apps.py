from django.apps import AppConfig
from django.contrib.auth.signals import user_logged_in


class UsersConfig(AppConfig):
    """AppConfig for the Users app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        """Import signals."""
        import users.signals

        user_logged_in.connect(users.signals.update_last_visit)
