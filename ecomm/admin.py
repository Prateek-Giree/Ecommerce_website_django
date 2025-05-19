from django.contrib import admin
from .models import Category, Vendor, Product
from .models import Wishlist, Review, UserProfile, Cart, CartItem


# Register your models here.
admin.site.register(Category)
admin.site.register(Vendor)
admin.site.register(Product)

admin.site.register(Wishlist)
admin.site.register(Review)
admin.site.register(UserProfile)
admin.site.register(Cart)
admin.site.register(CartItem)
