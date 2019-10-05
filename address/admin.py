from django.contrib import admin
from .models import (
    Region, Province,
    City, Barangay
)
# Register your models here.
admin.site.register((Region,Province,City,Barangay))
