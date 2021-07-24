from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError

from .models import User


# Create your views here.

def index(request):
	return render(request, "keepittidy/index.html")


def login(request):
	return render(request, "keepittidy/login.html")


def register(request):
	if request.method == "POST":
		username = request.POST["inputUser"]
		password = request.POST["inputPassword"]
		re_password = request.POST["inputRePassword"]

		# Check if password and re_password match
		if password != re_password:
			return render(request, "keepittidy/register.html", {"error_msg": "Make sure the passwords match!"})

		# Try to create new user
		try:
			user = User.objects.create_user(username=username, password=password)
			user.save()
		except IntegrityError:
			return render(request, "keepittidy/register.html", {"error_msg": "Sorry, username already taken by someone else."})

		return HttpResponseRedirect(reverse("index"))



	else:
		return render(request, "keepittidy/register.html")