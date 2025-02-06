from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="category", null=True, blank=True)

    def __str__(self):
        return self.name


from django.db import models


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    address = models.TextField()
    image = models.ImageField(upload_to="vendors/")

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    new_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/")
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
