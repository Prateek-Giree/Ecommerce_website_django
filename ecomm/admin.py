from django.contrib import admin
from .models import Category, Vendor, Product
from .models import Wishlist, Review, UserProfile, Cart, CartItem, DeliveryAddress,Order,OrderItem



class ProductAdmin(admin.ModelAdmin):
    class Media:
        js = ('js/admin_validator.js',) 
        css = {
            'all': ('css/admin_validator.css',)
        }

class CategoryAdmin(admin.ModelAdmin):
    class Media:
        js = ('js/admin_validator.js',) 
        css = {
            'all': ('css/admin_validator.css',)
        }

class DeliveryAddressAdmin(admin.ModelAdmin):
    class Media:
        js = ('js/admin_validator.js',) 
        css = {
            'all': ('css/admin_validator.css',)
        }

# Register your models here.
admin.site.register(Vendor)
admin.site.register(Category,CategoryAdmin)
admin.site.register(DeliveryAddress,DeliveryAddressAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)


admin.site.register(Wishlist)
admin.site.register(Review)
admin.site.register(UserProfile)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderItem)
