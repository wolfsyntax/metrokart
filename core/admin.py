from django.contrib import admin

# Register your models here.
from .models import (
    Category,Product
)
#app_name = "Product"
admin.site.site_header = 'Marketplace Administration'
admin.site.empty_value_display = '(None)'
admin.site.index_title = "Administrator"
admin.site.register((Category,Product))
#admin.site.register(Category)