from django.contrib import admin

# Register your models here.
from .models import (
    Address, UserProfile
)

admin.site.register((Address, UserProfile))