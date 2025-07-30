from django.contrib import admin
from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about, name="about"),


    path("products/<int:pk>/", views.products, name="products"),

    path("register/", views.register, name="register"),
    path('login/',views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path("cart/", views.cart, name="cart"),
    path("remove_from_cart/<int:pk>", views.remove_from_cart, name="remove_from_cart"),

    path("wishlist",views.wishlist, name="wishlist"),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    path("profile/<int:pk>" , views.profile, name="profile"),
    path("edit_profile" , views.edit_profile, name="edit_profile"),

    path("category/<int:pk>",views.category_page,name="category"),
    path("analytics", views.analytics_view, name="admin-analytics"),
]
