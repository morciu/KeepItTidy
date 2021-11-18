from django.test import TestCase

from .models import User, Collection, TextField, BooleanField, DateField, NumberField, DecimalField, ImageField, FieldDict, FieldNameTypePair, Item


# Create your tests here.
class CollectionTestCase(TestCase):
	def setUp(self):
		user = User.objects.create(username="morciu")

		col_1 = Collection.objects.create(user=user, name="Collection 1", description="Stuff and stuff")
		col_2 = Collection.objects.create(user=user, name="Collection 2")

		item_1 = Item.objects.create(user=user, name="item 1", description="description for item 1", collection=col_1)

	def test_col_existence(self):
		user = User.objects.get(username="morciu")
		cols = Collection.objects.filter(user=user)
		self.assertEqual(cols.count(), 2)

	def test_item(self):
		user = User.objects.get(username="morciu")
		col_1 = Collection.objects.get(user=user, name="Collection 1")
		item = Item.objects.filter(user=user, collection=col_1)
		self.assertEqual(item.count(), 1)
