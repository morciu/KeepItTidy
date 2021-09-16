import json
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import User, Collection, TextField, BooleanField, DateField, NumberField, DecimalField, FieldDict, FieldNameTypePair, Item

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
	items = {}

	

	return render(request, "keepittidy/view_collection.html")

@login_required
def create_collection(request):
	if request.method == "POST":

		# Get Collection Name and Description
		collection_name = request.POST["collectionName"]
		description = request.POST["description"]

		# Create instance of new collection object
		new_collection = Collection(user=request.user, name=collection_name, description=description)

		# Prepare dictionary for custom fields
		fields_dict = {}

		# Loop through custom fields created by user (current limit is 20)
		# Each fieldName and fieldType added will be numbered
		for i in range(1,20):
			if request.POST.get(f"fieldName{i}", False):
				# Create single pair dictionary for fieldName and fieldType
				field_dict = {}
				field_dict[request.POST[f"fieldName{i}"]] = request.POST.get(f"fieldType{i}")

				# Add the single pair dict to the main fields dictionary
				fields_dict[f'field{i}'] = field_dict
			else:
				# End loop when no more fields are detected
				break
		
		# Save new collection object
		new_collection.save()

		# Create an object for the dictionary model (used to store fieldName and fieldType pairs)
		field_dict_model = FieldDict(name=f"{collection_name} fields", collection=new_collection)
		field_dict_model.save()

		# Loop through fields_dict and create objects for key/value pair models to be connected to the dictionary model used above
		for field in fields_dict:
			for key, value in fields_dict[field].items():
				name_type_pair = FieldNameTypePair(dictionary=field_dict_model, field_name=key, field_type=value)
				name_type_pair.save()
		
		return render(request, "keepittidy/create_collection.html")
	else:
		return render(request, "keepittidy/create_collection.html")


@login_required
def get_collections(request):
	current_user = request.user
	collections = Collection.objects.filter(user=current_user)

	'''for i in collections:
		print(i.find_fields())'''
	
	return JsonResponse([collection.serialize() for collection in collections], safe=False)


@login_required
def add_item(request, collection_id):
	current_user = request.user
	collection = Collection.objects.get(id=collection_id)
	
	# Get collection fields
	field_dict = FieldDict.objects.get(collection=collection)
	fields = FieldNameTypePair.objects.filter(dictionary=field_dict)

	if request.method == "POST":

		# Get the Name and optional Description fields

		item_name = request.POST["itemName"]
		if request.POST["itemDescription"]:
			item = Item(name=item_name, description=request.POST["itemDescription"], user=current_user, collection=collection)
		else:
			item = Item(name=item_name, user=current_user, collection=collection)
		item.save()

		# Get the additional custom fields

		posts = request.POST.items()
		
		for key, value in posts:

			# Get field name
			field_name = key.split(" / ")[0]
			
			# Get field type
			field_type = key.split(" / ")[-1]

			# Check field type and create item accordingly
			if field_type == "text":
				field_obj = TextField(name=field_name, collection=collection, item=item, text=value)
				field_obj.save()
			elif field_type == "boolean":
				print(value)
				if value == "true":
					field_obj = BooleanField(name=field_name, collection=collection, item=item, boolean=True)
				elif value == "false":
					field_obj = BooleanField(name=field_name, collection=collection, item=item, boolean=False)
				field_obj.save()
			elif field_type == "date":
				field_obj = DateField(name=field_name, collection=collection, item=item, date=datetime.strptime(value, "%Y-%m-%d"))
				field_obj.save()
			elif field_type == "number":
				field_obj = NumberField(name=field_name, collection=collection, item=item, number=int(value))
				field_obj.save()
			elif field_type == "decimal":
				field_obj = DecimalField(name=field_name, collection=collection, item=item, decimal=float(value))
				field_obj.save()

			

		return render(request, 'keepittidy/add_item.html', {
			"user": current_user,
			"collection": collection,
			"fields": fields
			})
	else:
		

		return render(request, 'keepittidy/add_item.html', {
			"user": current_user,
			"collection": collection,
			"fields": fields
			})


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