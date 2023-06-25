from typing import Any

import msal
import requests
from django.conf import settings
from django.contrib.auth import login as django_login
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.http.request import HttpRequest
from dotenv import load_dotenv

from .models import User

load_dotenv()

# Create auth backend with django.contrib.auth.backends.ModelBackend as parent class

# MS auth settings
MY_HOST = settings.MICROSOFT_MY_HOST

APP_ID = settings.MICROSOFT_APP_ID
APP_SECRET = settings.MICROSOFT_APP_SECRET
TENANT_DOMAIN = settings.MICROSOFT_TENANT_DOMAIN

REDIRECT = settings.MICROSOFT_REDIRECT
SCOPES = settings.MICROSOFT_SCOPES
AUTHORITY = settings.MICROSOFT_AUTHORITY
LOGOUTURL = settings.MICROSOFT_LOGOUTURL

GRAPH_ENDPOINT = settings.MICROSOFT_GRAPH_ENDPOINT


class MicrosoftAuthBackend(BaseBackend):
    """MicrosoftAuthBackend A custom authentication backend for Microsoft authentication.

    Args:
        BaseBackend (_type_): Django's base authentication backend to extend.

    Returns:
        MicrosoftAuthBackend: The authentication backend.
    """

    def __init__(self) -> None:
        self.ms_client = msal.ConfidentialClientApplication(
            APP_ID, authority=AUTHORITY, client_credential=APP_SECRET
        )
        super().__init__()

    SESSION_KEY = "microsoft_auth"
    AUTH = "Microsoft"

    def setup(self, request: HttpRequest) -> None:
        """setup Set up the backend by creating a flow and storing it in the session.

        Args:
            request (HttpRequest): The request object.
        """
        if request.session.get(self.SESSION_KEY):
            request.session[self.SESSION_KEY] = {}
        flow = self.ms_client.initiate_auth_code_flow(
            SCOPES, redirect_uri=REDIRECT, domain_hint=TENANT_DOMAIN
        )

        self._store_to_session(request, "flow", flow)

    def get_auth_uri(self, request: HttpRequest) -> str:
        """get_auth_uri Get the auth URI from the session.

        Args:
            request (HttpRequest): The request object.

        Returns:
            str: The auth URI.
        """
        self.setup(request)
        return self._get_from_session(request, "flow")["auth_uri"]

    def authenticate(
        self,
        request: HttpRequest,
        **kwargs: Any,
    ) -> AbstractBaseUser | None:
        """authenticate Authenticate the user by getting the token from the auth code flow.

        Args:
            request (HttpRequest): The request object.

        Returns:
            AbstractBaseUser | None: The user object if authenticated, None otherwise.
        """
        # Dont authenticate if there is no request or no code in the request
        if not request or not request.GET.get("code"):
            return None

        flow = request.session.get(self.SESSION_KEY, {}).get("flow")
        if not flow:
            return None

        try:
            token = self.ms_client.acquire_token_by_auth_code_flow(flow, request.GET)
        except ValueError:
            return None

        if not token.get("access_token"):
            return None

        ms_user = requests.get(
            f"{GRAPH_ENDPOINT}/me",
            headers={"Authorization": f"Bearer {token['access_token']}"},
        ).json()

        # Check that the email is the tenant domain
        if ms_user["mail"].split("@")[1] != TENANT_DOMAIN:
            return None

        user = self._get_create_user(ms_user)
        if self.user_can_authenticate(user):
            return user

        return None

    def login(self, request: HttpRequest, user: User) -> None:
        """login Log the user in.

        Args:
            request (HttpRequest): The request object.
            user (User): The user object.
        """
        django_login(request, user)

    def logout(self, request: HttpRequest) -> None:
        """logout Log the user out.

        Args:
            request (HttpRequest): The request object.
        """
        self._delete_from_session(request, "flow")

    # OTHER HELPER METHODS

    def get_user(self, user_id: int) -> AbstractBaseUser | None:
        """get_user Get the user object.

        Args:
            user_id (int): The user id.

        Returns:
            AbstractBaseUser | None: The user object if found, None otherwise.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def user_can_authenticate(self, user: User) -> bool:
        """user_can_authenticate Check if the user can authenticate.

        Args:
            user (User): The user object.

        Returns:
            bool: True if the user can authenticate, False otherwise.
        """
        return user.can_login()

    def _get_create_user(self, ms_user: dict[str, Any]) -> User:
        """_get_create_user Get or create the user.

        Args:
            ms_user (dict[str, Any]): The user object from Microsoft Graph.

        Returns:
            User: The found/created user object.
        """
        try:
            user = User.objects.get(email=ms_user["mail"])
            return user
        except User.DoesNotExist:
            username = ms_user["mail"].split("@")[0]
            return User.objects.create(
                username=f"{username}",
                email=ms_user["mail"],
                first_name=ms_user["givenName"],
                last_name=ms_user["surname"],
            )

    def _store_to_session(self, request: HttpRequest, key: str, value: Any) -> None:
        """_store_to_session Store a value in the session using the SESSION_KEY.

        Args:
            request (HttpRequest): The request object.
            key (str): The key to store the value under.
            value (Any): The value to store.
        """
        if self.SESSION_KEY not in request.session:
            request.session[self.SESSION_KEY] = {}
        request.session[self.SESSION_KEY][key] = value

    def _get_from_session(self, request: HttpRequest, key: str) -> Any:
        """_get_from_session Get a value from the session using the SESSION_KEY.

        Args:
            request (HttpRequest): The request object.
            key (str): The key to get the value from.

        Returns:
            Any: The value from the session.
        """
        if self.SESSION_KEY not in request.session:
            return None
        return request.session[self.SESSION_KEY].get(key)

    def _delete_from_session(self, request: HttpRequest, key: str) -> None:
        """_delete_from_session Delete a value from the session using the SESSION_KEY.

        Args:
            request (HttpRequest): The request object.
            key (str): The key to delete the value from.
        """
        if self.SESSION_KEY not in request.session:
            return
        del request.session[self.SESSION_KEY][key]
