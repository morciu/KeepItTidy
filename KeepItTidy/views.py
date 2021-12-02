import json
from datetime import datetime
import os
from io import BytesIO

import xlrd
import xlwt

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ObjectDoesNotExist

from .models import User, Collection, TextField, BooleanField, DateField, NumberField, DecimalField, ImageField, FieldDict, FieldNameTypePair, Item

# Create your views here.


def index(request):
	if request.user.is_authenticated:
		collections = Collection.objects.filter(user=request.user)
		if collections.count() > 0:
			return HttpResponseRedirect(reverse("view_collection"))
		else:
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

			# Check if 'Remember me' was checked - if so remember password for next time
			remember_me = request.POST.get('rememberMe', False)
			if not remember_me:
				request.session.set_expiry(0)

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
		fields_dict = get_fields_dict(request)
		
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
def excel_import(request):
	if request.method == "POST":
		# Get the name and description for the collection
		collection_name = request.POST.get("collectionName")
		collection_description = request.POST.get("description")

		# Create instance of new collection object
		new_collection = Collection(user=request.user, name=collection_name, description=collection_description)

		# Get the main Name and Description fields for each item
		item_name = request.POST.get("itemName")
		item_description = request.POST["itemDescription"]

		# Get data from imported table

		if len(request.FILES) > 0:
			table = read_xls(request)
			
			# Loop through "Additional Fields" entered by the user and extract them from the imported table
			fields_dict = get_fields_dict(request)

			# Save new collection object
			new_collection.save()

			# Create an object for the dictionary model (used to store fieldName and fieldType pairs)
			field_dict_model = FieldDict(name=f"{collection_name} fields", collection=new_collection)
			field_dict_model.save()

			# Loop through fields_dict and create objects for key/value pair models to be connected to the dictionary model used above
			for field in fields_dict:
				for key, value in fields_dict[field].items():
					if isinstance(key, str):
						key = key.strip().title()
					name_type_pair = FieldNameTypePair(dictionary=field_dict_model, field_name=key, field_type=value)
					name_type_pair.save()

			# Loop through each item in the table, check if its field is valid and if so register it
			for item in table:
				name = None
				description = None

				# Get item name and item description
				for header, entry in item.items():
					if header.strip().lower() == item_name.strip().lower():
						name = entry.strip().title()
					if header.strip().lower() == item_description.strip().lower():
						description = entry.strip().title()
						new_item = Item(name=name, description=description, user=request.user, collection=new_collection)
						break

				if name and description:
					new_item = Item(name=name, description=description, user=request.user, collection=new_collection)
					new_item.save()
				elif name:
					new_item = Item(name=name, user=request.user, collection=new_collection)
					new_item.save()
				else:
					return render(request, "keepittidy/excel_import", {"error_msg": "ERROR!!!"})

				# Get additional fields
				for field in fields_dict:
					for key, value in fields_dict[field].items():
						for header, entry in item.items():
							if key.strip().lower() == header.strip().lower():
								field_name = key.strip().title()
								field_type = value

								# Check field type and create item accordingly
								create_field_obj(new_item, entry, field_type, field_name, new_collection)
					

		return HttpResponseRedirect(reverse("index"))
	else:
		return render(request, "keepittidy/excel_import.html")


@login_required
def excel_export(request, collection_id):
	# Get user and collection objects
	current_user = request.user
	collection = Collection.objects.get(id=collection_id, user=current_user)
	fields = collection.find_fields()

	# Get items
	items = Item.objects.filter(collection=collection)

	# Set up a response response
	response = HttpResponse(content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = f'attachment;filename={collection.name}.xls'

	# Create a workbook file
	wb = xlwt.Workbook(encoding='utf-8')

	# Create worksheet in the workbook
	ws = wb.add_sheet(f"{collection.name}")

	# Set up Headers
	position = 0

	ws.write(0, position, collection.name)
	position += 1

	ws.write(0, position, f"{collection.description}")
	position += 1

	for field in fields:
		ws.write(0, position, field)
		position += 1

	# Set up Rows
	row_pos = 1

	for item in items:
		col_pos = 0
		ws.write(row_pos, col_pos, f"{item.name}")
		col_pos += 1
		ws.write(row_pos, col_pos, f"{item.description}")
		col_pos += 1

		for field in fields:
			if fields[field] == "text":
				print(item.name)
				field_obj = TextField.objects.get(item=item, name=field)
				ws.write(row_pos, col_pos, f"{field_obj.text}")
				col_pos += 1
			elif fields[field] == "boolean":
				field_obj = BooleanField.objects.get(item=item, name=field)
				ws.write(row_pos, col_pos, f"{field_obj.boolean}")
				col_pos += 1
			elif fields[field] == "date":
				field_obj = DateField.objects.get(item=item, name=field)
				ws.write(row_pos, col_pos, f"{field_obj.date}")
				col_pos += 1
			elif fields[field] == "number":
				field_obj = NumberField.objects.get(item=item, name=field)
				ws.write(row_pos, col_pos, f"{field_obj.number}")
				col_pos += 1
			elif fields[field] == "decimal":
				field_obj = DecimalField.objects.get(item=item, name=field)
				ws.write(row_pos, col_pos, f"{field_obj.decimal}")
				col_pos += 1
		row_pos += 1

	# Set up Output - BytesIO object
	output = BytesIO()

	# Save to stringIO obj
	wb.save(output)

	# Set position at the begining of StringIO obj
	output.seek(0)

	response.write(output.getvalue())

	return response


@login_required
def upload_images(request, collection_id):
	current_user = request.user
	collection = Collection.objects.get(id=collection_id)
	
	# Get collection fields
	field_dict = FieldDict.objects.get(collection=collection)
	fields = FieldNameTypePair.objects.filter(dictionary=field_dict)

	if request.method == "POST":
		associated_field = request.POST['selectedField']

		associated_field_obj = FieldNameTypePair.objects.get(field_name=associated_field)
		associated_field_type = associated_field_obj.field_type

		print(associated_field_type)

		if len(request.FILES) > 0:
			for i in request.FILES:
				for img_file in request.FILES.getlist(i):

					# Loop through items checking associated_field

					items = Item.objects.filter(collection=collection)

					# Check if the collection has Image fields, if not they need to be created

					collection_fields = FieldDict.objects.get(collection=collection)
					image_field = FieldNameTypePair.objects.filter(dictionary=collection_fields, field_type='image')
					print(image_field)

					if image_field.count() <= 0:
						print("FOUND IMAGE FIELD")
						name_type_pair = FieldNameTypePair(dictionary=collection_fields, field_name="Image", field_type='image')
						name_type_pair.save()

					for item in items:
						# Check if the image already exists for this item
						old_imgs = ImageField.objects.filter(item=item)
						file_names = []
						for img in old_imgs:
							file_names.append(img.file_name())

						if old_imgs.count() <= 0 or img_file.name not in file_names:
							if associated_field == "name":
								entry = item.name
							elif associated_field_type == "number":
								entry = str(NumberField.objects.get(item=item, name=associated_field).number)
							elif associated_field == 'text':
								entry = TextField.objects.get(item=item, name=associated_field).text

							# Find a field entry that has the file name in it or vice versa
							if img_file.name.split('.')[0] in entry or entry in img_file.name.split('.')[0]:
								# Create ImageField for that object
								new_img = ImageField(name="Image", collection=collection, item=item, image=img_file)
								new_img.save()
						else:
							pass

					

					# Get the item object

					


		return render(request, "keepittidy/upload_images.html", {
				"user": current_user,
				"collection": collection,
				"fields": fields
				})
	else:
		return render(request, "keepittidy/upload_images.html", {
				"user": current_user,
				"collection": collection,
				"fields": fields
				})


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
	collection = Collection.objects.get(id=item.collection.id)
	remove_imgs = request.POST.get('removeCurrentImgs', False)
	
	# Get collection fields
	field_dict = FieldDict.objects.get(collection=collection)
	fields = FieldNameTypePair.objects.filter(dictionary=field_dict)

	if request.method == "POST":
		# Check for modifications and update the item

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

		# Verify if user wants to remove old images associated to item
		if remove_imgs:
			for i in ImageField.objects.filter(item=item):
				i.delete()

		# Check for uploaded files
		
		if len(request.FILES) > 0:
			for i in request.FILES:
				file_name = i.split(" / ")[0]
				file_type = i.split(" / ")[-1]

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
			"images": ImageField.objects.filter(item=item),
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

def create_field_obj(item, value, field_type, field_name, collection, filter=None):
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
		field_obj.save()
	elif field_type == "number":
		field_obj = NumberField(name=field_name, collection=collection, item=item, number=int(value))
		field_obj.save()
	elif field_type == "decimal":
		if value != '':
			field_obj = DecimalField(name=field_name, collection=collection, item=item, decimal=float(value))
			field_obj.save()
		else:
			field_obj = DecimalField(name=field_name, collection=collection, item=item, decimal=float(0))
			field_obj.save()


def get_fields_dict(request):
	# Prepare dictionary for custom fields
		fields_dict = {}

		# Loop through custom fields created by user (current limit is 20)
		# Each fieldName and fieldType added will be numbered
		last_field_nr = 0
		for i in range(1,20):
			if request.POST.get(f"fieldName{i}", False):
				# Create single pair dictionary for fieldName and fieldType
				field_dict = {}
				field_dict[request.POST[f"fieldName{i}"]] = request.POST.get(f"fieldType{i}")

				# Add the single pair dict to the main fields dictionary
				fields_dict[f'field{i}'] = field_dict
				last_field_nr = i
			else:
				# End loop when no more fields are detected
				break

		# Add an image field to all collections with the standard name "Image" (This was optional before but I think it was a mistake)
		field_dict = {"Image": "image"}
		fields_dict[f'field{last_field_nr+1}'] = field_dict

		return fields_dict


def read_xls(request):
	# Read data from uploaded xls file and return list 'table' with everything organized

	table = []

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
					# Check if the entry is a string, if so apply strip() and title()
					if isinstance(sheet.cell_value(row, col), str):
						item[headers[col].strip().title()] = sheet.cell_value(row, col).strip().title()
					else:
						item[headers[col].strip().title()] = sheet.cell_value(row, col)
				table.append(item)

	return table