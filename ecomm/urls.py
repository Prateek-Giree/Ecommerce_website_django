from django.contrib import admin
from django.urls import path
from .views import index,products,cart, login_view,register
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", index, name="index"),
    path("products/<int:pk>/", products, name="products"),
    path("register/", register, name="register"),
    path('login/',login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
