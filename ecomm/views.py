from django.shortcuts import render
from .models import Category, Product
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
    try:
        product = product[0]
    except IndexError:
        product = None
    if product is None:
        return render(request, "ecomm/404.html")
    if product.new_price and product.price:
        product.discount_percentage = (
            (product.price - product.new_price) / product.price
        ) * 100
    else:
        product.discount_percentage = 0 

        
    context = {
        "product": product,
    }
    return render(request, "ecomm/products.html", context)
