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
			"fields": self.find_fields()
		}

	def find_fields(self):
		# Return a dictionary for the fields related to this collection to be used in serialize()

		field_dict = FieldDict.objects.get(collection=self)
		fields = FieldNameTypePair.objects.filter(dictionary=field_dict)

		dictionary = {}

		for i in fields:
			dictionary[i.field_name] = i.field_type

		return dictionary


class TextField(models.Model):
	name = models.CharField(max_length=200)
	collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="text_field", null=True)
	text = models.CharField(max_length=500)


class DescriptionField(models.Model):
	name = models.CharField(max_length=200)
	collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="description_field", null=True)
	text = models.TextField(null=True)


class DateField(models.Model):
	name = models.CharField(max_length=200)
	collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="date_field", null=True)
	date = models.DateField(null=True)


class NumberField(models.Model):
	name = models.CharField(max_length=200)
	collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="number_field", null=True)
	number = models.IntegerField(null=True)


class DecimalField(models.Model):
	name = models.CharField(max_length=200)
	collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="decimal_field", null=True)
	decimal = models.DecimalField(max_digits=5, decimal_places=2)


class FieldDict(models.Model):
	collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="collection_fields", null=True)
	name = models.CharField(max_length=200)


class FieldNameTypePair(models.Model):
	dictionary = models.ForeignKey(FieldDict, on_delete=models.CASCADE, related_name="name_type_pair")
	field_name = models.CharField(max_length=200)
	field_type = models.CharField(max_length=200)