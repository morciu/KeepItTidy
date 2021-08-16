from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
	pass


class Collection(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="collection")
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=200)


class TextField(models.Model):
	name = models.CharField(max_length=200)
	collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="text_field", null=True)
	text = models.CharField(max_length=500)


class DescriptionField(models.Model):
	name = models.CharField(max_length=200)
	collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="description_field", null=True)
	text = models.TextField()


class DateField(models.Model):
	name = models.CharField(max_length=200)
	collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="date_field", null=True)
	date = models.DateField()


class NumberField(models.Model):
	name = models.CharField(max_length=200)
	collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="number_field", null=True)
	number = models.IntegerField()


class DecimalField(models.Model):
	name = models.CharField(max_length=200)
	collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="decimal_field", null=True)
	decimal = models.DecimalField(max_digits=5, decimal_places=2)