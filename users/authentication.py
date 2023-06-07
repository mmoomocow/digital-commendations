from django.conf import settings
from django.contrib import auth
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.views.decorators.debug import sensitive_variables

BACKEND_PATH = "users.ms_auth_backend.MS_auth_backend"

if BACKEND_PATH not in settings.AUTHENTICATION_BACKENDS:
    raise ImproperlyConfigured(f"{BACKEND_PATH} is not in AUTHENTICATION_BACKENDS")

BACKEND = auth.load_backend(BACKEND_PATH)


@sensitive_variables("creds")
def authenticate(request, **creds):
    try:
        user = BACKEND.authenticate(request)
    except PermissionDenied:
        return None

    if user is not None:
        user.backend = BACKEND_PATH
        return user
