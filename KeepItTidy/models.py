from django.db import models
from django.contrib.auth.models import AbstractUser

from datetime import datetime

import os

# Create your models here.
class User(AbstractUser):
	pass


class Collection(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="collection")
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=200)


	def delete(self, *args, **kwargs):
		# Delete local files for every image model

		items = Item.objects.filter(collection=self)

		for item in items:
			if len(ImageField.objects.filter(item=item)) > 0:
				for image_field in ImageField.objects.filter(item=item):
					os.remove(image_field.image.path)

		# Delete model
		super().delete(*args, **kwargs) # Calling the regular delete function


	def serialize(self):
		# Serialize model information in a JSON object

		return {
			"id": self.id,
			"user": self.user.username,
			"name": self.name,
			"description": self.description,
			"fields": self.find_fields(),
			"items": self.find_items()
		}

	def find_fields(self):
		# Return a dictionary for the fields related to this collection to be used in serialize()

		field_dict = FieldDict.objects.get(collection=self)
		fields = FieldNameTypePair.objects.filter(dictionary=field_dict)

		dictionary = {}

		for i in fields:
			dictionary[i.field_name] = i.field_type

		return dictionary

	def find_items(self):
		# Query for all items in collection

		items = Item.objects.filter(collection=self)
		item_fields = []

		for item in items:
			item_fields.append(item.get_fields())

		return item_fields


class Item(models.Model):
	name = models.CharField(max_length=200, default="item_name")
	description = models.TextField(max_length=400, null=True)

	# Foreign keys
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="item")
	collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="item")

	def delete(self, *args, **kwargs):
		# Delete local files before deleteing model
		if len(ImageField.objects.filter(item=self)) > 0:
			for i in ImageField.objects.filter(item=self):
				os.remove(i.image.path)

		# Delete model
		super().delete(*args, **kwargs) # Calling the regular delete function

	def get_fields(self):
		# Get all fields attached to this item
		fields = {"id": self.id, "name": self.name, "description": self.description, "col_id": self.collection.id}

		text_fields = TextField.objects.filter(item=self)
		if len(text_fields) > 0:
			for i in text_fields:
				fields[i.name] = i.text

		boolean_fields = BooleanField.objects.filter(item=self)
		if len(boolean_fields) > 0:
			for i in boolean_fields:
				fields[i.name] = i.boolean

		date_fields = DateField.objects.filter(item=self)
		if len(date_fields) > 0:
			for i in date_fields:
				fields[i.name] = i.date.strftime("%Y-%m-%d")

		number_fields = NumberField.objects.filter(item=self)
		if len(number_fields) > 0:
			for i in number_fields:
				fields[i.name] = i.number

		decimal_fields = DecimalField.objects.filter(item=self)
		if len(decimal_fields) > 0:
			for i in decimal_fields:
				fields[i.name] = i.decimal

		image_fields = ImageField.objects.filter(item=self)
		if len(image_fields) > 0:

			# Store all image urls in a list in case an item uses multiple images
			image_urls = []

			for i in image_fields:
				image_urls.append(i.image.url)

			fields[i.name] = image_urls # This dictionary object will return an array of urls
		else:
			# Return an empty ulr list, will catch this in javascript and load a placeholder image
			fields["img_missing"] = []

		return fields


class TextField(models.Model):
	name = models.CharField(max_length=200)
	collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="text_field")
	item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="text_field")
	text = models.CharField(max_length=500)


class BooleanField(models.Model):
	name = models.CharField(max_length=200)
	collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="boolean_field")
	item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="boolean_field")
	boolean = models.BooleanField(default=False)


class DateField(models.Model):
	name = models.CharField(max_length=200)
	collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="date_field")
	item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="date_field")
	date = models.DateField(null=True)


class NumberField(models.Model):
	name = models.CharField(max_length=200)
	collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="number_field")
	item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="number_field")
	number = models.IntegerField(null=True)


class DecimalField(models.Model):
	name = models.CharField(max_length=200)
	collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="decimal_field")
	item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="decimal_field")
	decimal = models.DecimalField(max_digits=1000, decimal_places=2)


class ImageField(models.Model):
	name = models.CharField(max_length=200)
	collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="image_field")
	item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="image_field")
	image = models.ImageField(upload_to='images/')

	def file_name(self):
		# Return the name of the file
		return os.path.basename(self.image.name)

	def delete(self, *args, **kwargs):
		# Delete local files image model before deleting model
		os.remove(self.image.path)

		# Delete model
		super().delete(*args, **kwargs) # Calling the regular delete function



# Set up a dictionary through models for storing field_name and field_type pairs

class FieldDict(models.Model):
	collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="collection_fields")
	name = models.CharField(max_length=200)


class FieldNameTypePair(models.Model):
	dictionary = models.ForeignKey(FieldDict, on_delete=models.CASCADE, related_name="name_type_pair")
	field_name = models.CharField(max_length=200)
	field_type = models.CharField(max_length=200)

