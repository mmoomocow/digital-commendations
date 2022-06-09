from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.shortcuts import render
import os

# Create your views here.


@csrf_exempt
def KAMAR_check(request):
	# Respond to KAMAR check requests
	# https://directoryservices.kamar.nz/?listening-service/check

	# First check basic auth
	if request.META.get('HTTP_AUTHORIZATION') is None:
		return JsonResponse({
			"SMSDirectoryData": {
				"error": 403,
				"result": "No authentication provided",
				'service': 'Digital Commendation System',
				'version': '1.0'
			}
		}, status=403)
	elif (request.META.get('HTTP_AUTHORIZATION') == f'Basic {os.environ.get("KAMAR_AUTH_USERNAME")}/{os.environ.get("KAMAR_AUTH_PASSWORD")}'):
		return JsonResponse({
			"SMSDirectoryData": {
				"error": 0,
				"result": "OK",
				"service": "Digital Commendation System",
				"version": "1.0",
				"status": "Ready",
				"infourl": "https://127.0.0.1:8080",
				"privacystatement": "This service is still in development, and as a result doesn't store any data.",
				"options": {

				}
			}
		}, status=200)
	else:
		return JsonResponse(
			{
				"SMSDirectoryData": {
					"error": 403,
					"result": "Invalid authentication",
					'service': 'Digital Commendation System',
					'version': '1.0'
				}
			}, status=403)
