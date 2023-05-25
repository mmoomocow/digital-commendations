import os
from base64 import b64encode

from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


@csrf_exempt
def KAMAR_check(request) -> JsonResponse:
    """
    Authenticate and respond to KAMAR check requests
    https://directoryservices.kamar.nz/?listening-service/check
    """
    # Translate username password to HTTP basic auth
    token = b64encode(
        f"{os.environ.get('KAMAR_AUTH_USERNAME')}:{os.environ.get('KAMAR_AUTH_PASSWORD')}".encode(
            "utf-8"
        )
    ).decode("utf-8")
    expected_auth = f"Basic {token}"

    # First check basic auth
    if request.META.get("HTTP_AUTHORIZATION") is None:
        return JsonResponse(
            {
                "SMSDirectoryData": {
                    "error": 403,
                    "result": "No authentication provided",
                    "service": "Digital Commendation System",
                    "version": "1.0",
                }
            },
            status=403,
        )

    if request.META.get("HTTP_AUTHORIZATION") == expected_auth:
        return JsonResponse(
            {
                "SMSDirectoryData": {
                    "error": 0,
                    "result": "OK",
                    "service": "Digital Commendation System",
                    "version": "1.0",
                    "status": "Ready",
                    "infourl": "https://dcs.mgray.online/about/",
                    "privacystatement": "This service is still in development, please see https://dcs.mgray.online/privacy/ for more information.",
                    "options": {},
                }
            },
            status=200,
        )

    return JsonResponse(
        {
            "SMSDirectoryData": {
                "error": 403,
                "result": "Invalid authentication",
                "service": "Digital Commendation System",
                "version": "1.0",
            }
        },
        status=403,
    )
