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
	text = models.CharField(max_length=500)