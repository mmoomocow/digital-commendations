from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

# Create your views here.

def loginView(request):
	if request.method == 'POST':
		# Triggered if the client has filled out and submitted the form
		username = request.POST['username']
		password = request.POST['password']
		# Checks if the user is valid
		user = authenticate(request, username=username, password=password)
		if user is not None:
			# Restrict access to active teachers for now
			if user.is_active:
				login(request, user)
				return HttpResponse('<h1>Login successful</h1>')

	else:
		# Triggered if the client has not filled out the form, so send them the login page
		return HttpResponse('<h1>Login</h1>') # Basic HTTP response for now without a form, but we'll add one later
