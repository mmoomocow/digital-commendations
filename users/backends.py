import os
from typing import Any

import msal
import requests
from django.contrib.auth import login as django_login
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.http.request import HttpRequest
from dotenv import load_dotenv

from .models import User

load_dotenv()

# Create auth backend with django.contrib.auth.backends.ModelBackend as parent class

MY_HOST = os.getenv("MY_HOST")

APP_ID = os.getenv("MICROSOFT_AUTH_CLIENT_ID")
APP_SECRET = os.getenv("MICROSOFT_AUTH_CLIENT_SECRET")
TENANT_ID = os.getenv("MICROSOFT_AUTH_TENANT_ID")
TENANT_DOMAIN = os.getenv("MICROSOFT_AUTH_TENANT_DOMAIN")

REDIRECT = f"{MY_HOST}/users/callback/"
SCOPES = ["https://graph.microsoft.com/user.read"]
AUTHORITY = f"https://login.microsoftonline.com/common"  # TODO - Test with tenant_id
LOGOUTURL = f"{MY_HOST}/users/logout/"

GRAPH_ENDPOINT = "https://graph.microsoft.com/v1.0"


class MicrosoftAuthBackend(BaseBackend):
    SESSION_KEY = "microsoft_auth"
    AUTH = "Microsoft"

    def setup(self, request: HttpRequest) -> None:
        self.app = msal.ConfidentialClientApplication(
            APP_ID, authority=AUTHORITY, client_credential=APP_SECRET
        )
        flow = self.app.initiate_auth_code_flow(
            SCOPES, redirect_uri=REDIRECT
        )  # TODO - Test with domain_hint=TENANT_DOMAIN

        self._store_to_session(request, "flow", flow)

    def get_auth_uri(self, request: HttpRequest) -> str:
        self.setup(request)
        return self._get_from_session(request, "flow")["auth_uri"]

    def authenticate(
        self,
        request: HttpRequest,
        **kwargs: Any,
    ) -> AbstractBaseUser | None:
        flow = request.session.get(self.SESSION_KEY, {}).get("flow")
        if not flow:
            return None

        try:
            token = self.app.acquire_token_by_auth_code_flow(flow, request.GET.dict())
        except ValueError:
            return None

        if not token.get("access_token"):
            return None

        ms_user = requests.get(
            f"{GRAPH_ENDPOINT}/me",
            headers={"Authorization": f"Bearer {token['access_token']}"},
        ).json()

        user = self._get_create_user(ms_user)
        if self.user_can_authenticate(user):
            return user

        return None

    def login(self, request: HttpRequest, user: User) -> None:
        django_login(request, user)

    def logout(self, request: HttpRequest) -> None:
        self._delete_from_session(request, "flow")

    # OTHER HELPER METHODS

    def get_user(self, user_id: int) -> AbstractBaseUser | None:
        return super().get_user(user_id)

    def user_can_authenticate(self, user: User) -> bool:
        if user is None:
            return False
        is_active = getattr(user, "is_active", None)
        return is_active or is_active is None

    def _get_create_user(self, ms_user: dict[str, Any]) -> User:
        try:
            user = User.objects.get(email=ms_user["mail"])
            print(f"Found user: {user}")
            return user
        except User.DoesNotExist:
            print("User does not exist, creating")
            username = ms_user["mail"].split("@")[0]
            return User.objects.create(
                username=f"{username}",
                email=ms_user["mail"],
                first_name=ms_user["givenName"],
                last_name=ms_user["surname"],
            )

    def _store_to_session(self, request: HttpRequest, key: str, value: Any) -> None:
        request.session[self.SESSION_KEY][key] = value

    def _get_from_session(self, request: HttpRequest, key: str) -> Any:

    def _delete_from_session(self, request: HttpRequest, key: str) -> None:
        del request.session[self.SESSION_KEY][key]
