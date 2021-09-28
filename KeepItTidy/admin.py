from django.contrib import admin
from .models import User, Collection, TextField, BooleanField, DateField, NumberField, DecimalField, ImageField, FieldDict, FieldNameTypePair, Item

# Register your models here.
admin.site.register(User)
admin.site.register(Collection)
admin.site.register(TextField)
admin.site.register(BooleanField)
admin.site.register(DateField)
admin.site.register(NumberField)
admin.site.register(DecimalField)
admin.site.register(ImageField)
admin.site.register(FieldDict)
admin.site.register(FieldNameTypePair)
admin.site.register(Item)