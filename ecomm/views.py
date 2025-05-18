from django.shortcuts import render
from .models import Category, Product, Vendor
from django.db.models import Count

# Create your views here.


def index(request):
    categories = Category.objects.annotate(product_count=Count("product"))
    recent_products = Product.objects.order_by("-id")[:7]
    recent_50_products = Product.objects.order_by("-id")[:50]

    for product in recent_50_products:
        if product.new_price and product.price:
            product.discount_percentage = (
                (product.price - product.new_price) / product.price
            ) * 100
        else:
            product.discount_percentage = 0  # No discount if no new_price or price

    context = {
        "categories": categories,
        "recent_products": recent_products,
        "recent_50_products": recent_50_products,
    }
    return render(request, "ecomm/index.html", context)


def products(request,pk):
    
    product= Product.objects.filter(id=pk)
    categories = Category.objects.annotate(product_count=Count("product"))
    related_products = Product.objects.filter(category=product[0].category).exclude(id=pk)[:4]

    try:
        product = product[0]
    except IndexError:
        product = None
    if product is None:
        return render(request, "ecomm/404.html")
    # Calculate discount percentage for the main product
    if product.new_price and product.price:
        product.discount_percentage = (
            (product.price - product.new_price) / product.price
        ) * 100
    else:
        product.discount_percentage = 0 


    # Calculate discount percentage for related products
    for product in related_products:
        if product.new_price and product.price:
            product.discount_percentage = (
                (product.price - product.new_price) / product.price
            ) * 100
        else:
            product.discount_percentage = 0  # No discount if no new_price or price

    vendor = product.vendor
    
    context = {
        "product": product,
        "vendor": vendor,
        "categories": categories,
        "related_products": related_products,
    }
    return render(request, "ecomm/products.html", context)
