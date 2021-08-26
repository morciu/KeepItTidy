import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import User, Collection, TextField, DescriptionField, DateField, NumberField, DecimalField

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


@login_required
def view_collection(request):
	return render(request, "keepittidy/view_collection.html")

@login_required
def create_collection(request):
	if request.method == "POST":
		collection_name = request.POST["collectionName"]
		description = request.POST["description"]
		new_collection = Collection(user=request.user, name=collection_name, description=description)

		
		fields_dict = {}

		for i in range(1,5):
			if request.POST.get(f"fieldName{i}", False):
				field_dict = {}
				field_dict[request.POST[f"fieldName{i}"]] = request.POST.get(f"fieldType{i}")
				fields_dict[f'field{i}'] = field_dict
			else:
				break
		
		new_collection.save()

		for field in fields_dict:
			for key, value in fields_dict[field].items():
				field = create_field_obj(value, key, new_collection)
				field.save()
		
		return render(request, "keepittidy/create_collection.html")
	else:
		return render(request, "keepittidy/create_collection.html")


@login_required
def get_collections(request):
	current_user = request.user
	collections = Collection.objects.filter(user=current_user)
	print(current_user)
	print(collections)
	
	return JsonResponse([collection.serialize() for collection in collections], safe=False)


@login_required
def collection_page(request, collection_id):
	current_user = request.user

	return render(request, 'keepittidy/collection_page.html')


# General purpose functions

def create_field_obj(type, name, collection):
	if type == "text":
		return TextField(name=name, collection=collection)
	elif type == "description":
		return DescriptionField(name=name, collection=collection)
	elif type == "date":
		return DateField(name=name, collection=collection)
	elif type == "number":
		return NumberField(name=name, collection=collection)
	elif type == "decimal":
		return DecimalField(name=name, collection=collection)