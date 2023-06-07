import os

import msal
import requests
from django.contrib.auth import login as django_login
from django.contrib.auth.backends import BaseBackend
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
        # try:
        token = app.acquire_token_by_auth_code_flow(flow, request.GET)
        if token:
            ms_user = self._get_user(token)
            if ms_user:
                user = self._get_or_create_user(ms_user)
                if user:
                    return user
        return None

    def login(self, request, user):
        print("MS AUTH LOGGING IN")
        django_login(request, user)

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

    def _get_or_create_user(self, ms_user):
        try:
            user = User.objects.get(email=ms_user["mail"])
            print(f"Found user: {user}")
            return user
        except User.DoesNotExist:
            print("User does not exist, creating")
            username = ms_user["mail"].split("@")[0]
            return User.objects.create(
                username=f"{username}-ms",
                email=ms_user["mail"],
                first_name=ms_user["givenName"],
                last_name=ms_user["surname"],
            )
