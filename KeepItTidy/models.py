from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
	pass


class Collection(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="collection")
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=200)

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
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="item")
	collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="item")

	def get_fields(self):
		# Get all fields attached to this item
		fields = []

		text_fields = TextField.objects.filter(item=self)
		if len(text_fields) > 0:
			text_field_dict = {}
			for i in text_fields:
				text_field_dict[i.name] = i.text
			fields.append(text_field_dict)

		description_fields = DescriptionField.objects.filter(item=self)
		if len(description_fields) > 0:
			description_field_dict = {}
			for i in description_fields:
				description_field_dict[i.name] = i.text
			fields.append(description_field_dict)

		date_fields = DateField.objects.filter(item=self)
		if len(date_fields) > 0:
			date_field_dict = {}
			for i in date_fields:
				date_field_dict[i.name] = i.date
			fields.append(date_field_dict)

		number_fields = NumberField.objects.filter(item=self)
		if len(number_fields) > 0:
			number_field_dict = {}
			for i in number_fields:
				number_field_dict[i.name] = i.number
			fields.append(number_field_dict)

		decimal_fields = DecimalField.objects.filter(item=self)
		if len(decimal_fields) > 0:
			decimal_field_dict = {}
			for i in date_fields:
				decimal_field_dict[i.name] = i.decimal
			fields.append(description_field_dict)

		return fields


class TextField(models.Model):
	name = models.CharField(max_length=200)
	collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="text_field")
	item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="text_field")
	text = models.CharField(max_length=500)


class DescriptionField(models.Model):
	name = models.CharField(max_length=200)
	collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="description_field")
	item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="description_field")
	text = models.TextField(null=True)


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
	decimal = models.DecimalField(max_digits=5, decimal_places=2)


class FieldDict(models.Model):
	collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="collection_fields")
	name = models.CharField(max_length=200)


class FieldNameTypePair(models.Model):
	dictionary = models.ForeignKey(FieldDict, on_delete=models.CASCADE, related_name="name_type_pair")
	field_name = models.CharField(max_length=200)
	field_type = models.CharField(max_length=200)