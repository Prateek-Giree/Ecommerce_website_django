from django.contrib import admin
from django.urls import path
from .views import index,products,cart, login_view,register,profile,edit_profile,remove_from_cart,analytics_view,category_page
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", index, name="index"),
    path("products/<int:pk>/", products, name="products"),
    path("register/", register, name="register"),
    path('login/',login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path("cart/", cart, name="cart"),
    path("remove_from_cart/<int:pk>", remove_from_cart, name="remove_from_cart"),
    path("profile/<int:pk>" , profile, name="profile"),
    path("edit_profile" , edit_profile, name="edit_profile"),
    path("category/<int:pk>",category_page,name="category"),
    path("analytics", analytics_view, name="admin-analytics"),
]
