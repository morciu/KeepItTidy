from django.contrib import admin
from .models import User, Collection, TextField, DescriptionField, DateField, NumberField, DecimalField

# Register your models here.
admin.site.register(User)
admin.site.register(Collection)
admin.site.register(TextField)
admin.site.register(DescriptionField)
admin.site.register(DateField)
admin.site.register(NumberField)
admin.site.register(DecimalField)