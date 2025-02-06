from django.contrib import admin
from .models import Category, Vendor, Product, User


# Register your models here.
admin.site.register(Category)
admin.site.register(Vendor)
admin.site.register(Product)
admin.site.register(User)