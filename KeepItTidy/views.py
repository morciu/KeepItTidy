import json
from datetime import datetime
import os

import xlrd

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Collection, TextField, BooleanField, DateField, NumberField, DecimalField, ImageField, FieldDict, FieldNameTypePair, Item, TempCollection

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
def view_collection(request, collection_id=None):
	
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
def excel_import_1(request):
	if request.method == "POST":
		collection_name = request.POST.get("collectionName")
		collection_description = request.POST.get("description")

		print(request.FILES)

		if len(request.FILES) > 0:

			table = []

			print("There be files!")
			for i in request.FILES:
				for file in request.FILES.getlist(i):
					if file.name.split(".")[1] != "xls":
						return render(request, "keepittidy/excel_import_1.html", {
							"error" : "Invalid file format, please upload an 'xls' file."
							})

					# Handling XLS file contents

					# Open xls file
					wb = xlrd.open_workbook(file_contents=file.read())
					sheet = wb.sheet_by_index(0)

					# Get table headers
					headers = []

					for h_index in range(sheet.ncols):
						headers.append(sheet.cell_value(0, h_index))

					for row in range(1, sheet.nrows):
						item = {}
						for col in range(sheet.ncols):
							#print(f"{headers[col]}: {sheet.cell_value(row, col)}")

							item[headers[col]] = sheet.cell_value(row, col)
						table.append(item)
						#print("\n")
				
				temp_collection = TempCollection(user=request.user, name=collection_name, description=collection_description,\
				 headers=json.dumps(headers), table=json.dumps(table))
				temp_collection.save()

		return HttpResponseRedirect(reverse("excel_import_2"))
	else:
		return render(request, "keepittidy/excel_import_1.html")


@login_required
def excel_import_2(request):
	jsonDec = json.decoder.JSONDecoder()
	try:
		temp_collection = TempCollection.objects.get(user=request.user)
		context = {
			"collection_name": temp_collection.name,
			"collection_description": temp_collection.description,
			"headers": jsonDec.decode(temp_collection.headers),
			"table": jsonDec.decode(temp_collection.table)
			}
		
	except TempCollection.DoesNotExist:
		print("DOES NOT EXist")
		return HttpResponseRedirect(reverse("excel_import_1"))

	if request.method == "POST":
		# Ask which are the main "Name" and "Description" fields
		name_field = request.POST["itemName"]
		description_field = request.POST.get("itemDescription")

		# Create instance of new collection object
		new_collection = Collection(user=request.user, name=context["collection_name"], description=context["collection_description"])

		fields_dict = {}

		print(name_field)

		# Loop through headers found in the imported table
		# Each fieldName and fieldType added will be numbered
		for i in range(1, len(context["headers"])+1):
			if request.POST.get(f"fieldName{i}", False):
				# Create single pair dictionary for fieldName and fieldType
				field_dict = {}
				if request.POST[f'fieldName{i}'] != name_field:
					field_dict[request.POST[f"fieldName{i}"]] = request.POST.get(f'fieldType{i}')

				# Add the single pair dict to the main fields dictionary
				fields_dict[f'field{i}'] = field_dict

		print(fields_dict)

		# Save new collection object
		new_collection.save()

		# Create an object for the dictionary model (used to store fieldName and fieldType pairs)
		field_dict_model = FieldDict(name=f"{context['collection_name']} fields", collection=new_collection)
		field_dict_model.save()

		# Loop through fields_dict and create objects for key/value pair models to be connected to the dictionary model used above
		for field in fields_dict:
			for key, value in fields_dict[field].items():
				print(f"{key}: {value}")
				name_type_pair = FieldNameTypePair(dictionary=field_dict_model, field_name=key, field_type=value)
				name_type_pair.save()

		#new_collection.delete()


		# Delete the temporary model
		temp_collection.delete()

		return render(request, "keepittidy/excel_import_2.html", context)
	else:
		return render(request, "keepittidy/excel_import_2.html", context)


@login_required
def delete_collection(request):
	if request.method == "PUT":
		# Get JSON data from delete button
		data = json.loads(request.body)

		# Instantiate collection that will be deleted
		col_to_del = Collection.objects.get(id=data['collectionId'])
		print("deleted collection from db")
		col_to_del.delete()

		return render(request, "keepittidy/view_collection.html")


@login_required
def get_collections(request):
	current_user = request.user
	collections = Collection.objects.filter(user=current_user)
	
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
			create_field_obj(item, value, field_type, field_name, collection)

		# Check if any files were uploaded
		if len(request.FILES) > 0:
			for i in request.FILES:
				file_name = i.split(" / ")[0]
				file_type = i.split(" / ")[-1]

				for file in request.FILES.getlist(i):
					if file_type == "image":
						image = file
						print(file)

						field_obj = ImageField(name=file_name, collection=collection, item=item, image=image)
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


def edit_item(request, item_id):
	current_user = request.user
	item = Item.objects.get(id=item_id)

	print(item.get_fields())

	collection = Collection.objects.get(id=item.collection.id)
	
	# Get collection fields
	field_dict = FieldDict.objects.get(collection=collection)
	fields = FieldNameTypePair.objects.filter(dictionary=field_dict)

	if request.method == "POST":
		#TO DO

		# Check for modifications anc update the item

		# Check if name has been changed
		if item.get_fields()['name'] == request.POST['itemName']:
			print("\nName hasn't changed\n")
		else:
			print("\nName has changed\n")
			item.name = request.POST['itemName']
			item.save()

		# Check if description has been changed
		if item.get_fields()['description'] == request.POST['itemDescription']:
			print("\nDescription hasn't changed\n")
		else:
			print("\nDescription hasn't changed\n")
			item.description = request.POST['itemDescription']
			item.save()

		posts = request.POST.items()
		
		for key, value in posts:
			if key != 'itemName' and key != 'itemDescription':
				print(f"{key}: {value}")

				# Get field name
				field_name = key.split(" / ")[0]
			
				# Get field type
				field_type = key.split(" / ")[-1]

				# Check field type and create object
				create_field_obj(item, value, field_type, field_name, collection)

		# Check for uploaded files
		
		if len(request.FILES) > 0:
			for i in request.FILES:
				file_name = i.split(" / ")[0]
				file_type = i.split(" / ")[-1]

				# Instantiate old image field objects
				old_img_objs = ImageField.objects.filter(item=item)

				# Remove each of the old img models associated with this item
				for img_model in old_img_objs:
					img_model.delete()

				# Loop through all newly uploaded files and create new ImageField objects associated with this item
				for file in request.FILES.getlist(i):
					if file_type == "image":
						image = file

						field_obj = ImageField(name=file_name, collection=collection, item=item, image=image)
						field_obj.save()
					

		return render(request, 'keepittidy/edit_item.html', {
			"item": item.get_fields(),
			"user": current_user,
			"collection": collection,
			"fields": fields
			})

	else:
		return render(request, 'keepittidy/edit_item.html', {
			"item": item.get_fields(),
			"user": current_user,
			"collection": collection,
			"fields": fields
			})


def delete_item(request):
	if request.method == "PUT":
		# Get JSON data from delete button
		data = json.loads(request.body)
		
		# Instantiate item that will be deleted
		item_to_del = Item.objects.get(id=data['itemId'])

		# Get parent collection to pass on as api and refresh the page
		parent_collection = item_to_del.collection.id
		print(parent_collection)

		# Delete object from database
		item_to_del.delete()

		return JsonResponse({"parrentCollectionId": parent_collection})

	return HttpResponseRedirect(reverse("index"))



# General purpose functions

def create_field_obj(item, value, field_type, field_name, collection):
	# Check field type and create field object accordingly
	if field_type == "text":
		field_obj = TextField(name=field_name, collection=collection, item=item, text=value)
		field_obj.save()
	elif field_type == "boolean":
		if value == "true":
			field_obj = BooleanField(name=field_name, collection=collection, item=item, boolean=True)
		elif value == "false":
			field_obj = BooleanField(name=field_name, collection=collection, item=item, boolean=False)
		field_obj.save()
	elif field_type == "date":
		field_obj = DateField(name=field_name, collection=collection, item=item, date=datetime.strptime(value, "%Y-%m-%d"))
		print(value)
		field_obj.save()
	elif field_type == "number":
		field_obj = NumberField(name=field_name, collection=collection, item=item, number=int(value))
		field_obj.save()
	elif field_type == "decimal":
		field_obj = DecimalField(name=field_name, collection=collection, item=item, decimal=float(value))
		field_obj.save()