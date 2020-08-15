from django.contrib import admin

# Register your models here.
from .models import Person , photo_data


# Register your models here.
admin.site.register(Person)
admin.site.register(photo_data)