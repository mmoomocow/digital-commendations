import os

import msal
import requests
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.base_user import AbstractBaseUser
from dotenv import load_dotenv

from .models import User

load_dotenv()

# Create auth backend with django.contrib.auth.backends.ModelBackend as parent class

MY_HOST = os.getenv("MY_HOST")

APP_ID = os.getenv("MICROSOFT_AUTH_CLIENT_ID")
APP_SECRET = os.getenv("MICROSOFT_AUTH_CLIENT_SECRET")
TENANT_ID = os.getenv("MICROSOFT_AUTH_TENANT_ID")

REDIRECT = f"{MY_HOST}/users/callback/"
SCOPES = ["https://graph.microsoft.com/user.read"]
AUTHORITY = "https://login.microsoftonline.com/common"
LOGOUTURL = f"{MY_HOST}/users/logout/"

GRAPH_ENDPOINT = "https://graph.microsoft.com/v1.0"


class MS_auth_backend(BaseBackend):
    SESSION_KEY = "MICROSOFT"
    AUTH = "MICROSOFT"

    def setup(self, request):
        app = self._get_confidential_app()
        flow = app.initiate_auth_code_flow(
            scopes=SCOPES, redirect_uri=REDIRECT, max_age=3600
        )
        self.save_to_store(request, flow)
        return flow["auth_uri"]

    def authenticate(self, request):
        flow = self.get_from_store(request)
        if not flow:
            return None
        app = self._get_confidential_app()
        try:
            token = app.acquire_token_by_auth_code_flow(flow, request.GET)
        except ValueError:
            return None
        if "error" in token:
            return None
        ms_user = self._get_user(token)
        if not ms_user:
            return None
        user, created = User.objects.get_or_create(
            username=ms_user["userPrincipalName"],
            defaults={
                "first_name": ms_user["givenName"],
                "last_name": ms_user["surname"],
                "email": ms_user["mail"],
            },
        )
        if self.user_can_authenticate(user):
            return user
        return None

    def get_user(self, user_pk):
        try:
            return User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            return None

    # Assorted helper functions
    def user_can_authenticate(self, user):
        is_active = getattr(user, "is_active", None)
        return is_active or is_active is None

    @classmethod
    def _get_confidential_app(cls):
        return msal.ConfidentialClientApplication(
            APP_ID, authority=AUTHORITY, client_credential=APP_SECRET
        )

    def save_to_store(self, request, data):
        request.session[self.SESSION_KEY] = data

    def get_from_store(self, request):
        return request.session.get(self.SESSION_KEY, {})

    def remove_from_store(self, request):
        request.session.pop(self.SESSION_KEY, None)

    @classmethod
    def _get_user(cls, token):
        access_token = token.get("access_token", "")
        req = requests.get(
            url=f"{GRAPH_ENDPOINT}/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        if req.status_code == requests.codes.ok:
            user = req.json()
            return user
        return None
