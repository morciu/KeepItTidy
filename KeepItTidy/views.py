from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout

from .models import User, Collection, TextField


# Create your views here.

def index(request):
	if request.user.is_authenticated:
		return render(request, "keepittidy/index.html")
	else:
		return HttpResponseRedirect(reverse("login"))


def login_view(request):
	if request.method == "POST":
		# Attempt to sign user in
		username = request.POST["inputUser"]
		password = request.POST["inputPassword"]
		user = authenticate(request, username=username, password=password)

		# Check if authenticated
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse("index"))
		else:
			return render(request, "keepittidy/login.html", {
				"error_msg": "Invalid login!"
				})
	else:
		return render(request, "keepittidy/login.html")


def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse("index"))


def register(request):
	if request.method == "POST":
		username = request.POST["inputUser"]
		password = request.POST["inputPassword"]
		re_password = request.POST["inputRePassword"]

		# Check if password and re_password match
		if password != re_password:
			return render(request, "keepittidy/register.html", {
				"error_msg": "Make sure the passwords match!"
				})

		# Try to create new user
		try:
			user = User.objects.create_user(username=username, password=password)
			user.save()
		except IntegrityError:
			return render(request, "keepittidy/register.html", {"error_msg": "Sorry, username already taken by someone else."})
		# Redirect to index page
		return HttpResponseRedirect(reverse("index"))
	else:
		return render(request, "keepittidy/register.html")


def create_collection(request):
	if request.method == "POST":
		collection_name = request.POST["collectionName"]
		description = request.POST["description"]
		field_name = request.POST["fieldName"]
		field_type = request.POST.get("fieldType")
		print(collection_name)
		print(description)
		print(field_name)
		print(field_type)

		new_collection = Collection(user=request.user, name=collection_name, description=description)
		if field_type == "text":
			new_field = TextField(name=field_name, collection=new_collection, text="butts butts butts")

		new_collection.save()
		new_field.save()

		
		return render(request, "keepittidy/create_collection.html")
	else:
		return render(request, "keepittidy/create_collection.html")