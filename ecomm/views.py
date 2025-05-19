from .models import Category, Product, Vendor,Cart, CartItem,Wishlist
from django.db.models import Count
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages



def register(request):
    page="register"
    context={
        "page": page,
    }
    return render(request, "ecomm/login_register.html",context)

def login(request):
    page="login"
    context={
        "page": page,
    }
    return render(request, "ecomm/login_register.html", context)

def index(request):
    categories = Category.objects.annotate(product_count=Count("product"))
    recent_products = Product.objects.order_by("-id")[:7]
    recent_50_products = Product.objects.order_by("-id")[:50]

    context = {
        "categories": categories,
        "recent_products": recent_products,
        "recent_50_products": recent_50_products,
    }
    return render(request, "ecomm/index.html", context)


def products(request, pk):
    product_qs = Product.objects.filter(id=pk)
    try:
        product = product_qs[0]
    except IndexError:
        return render(request, "ecomm/404.html")

    categories = Category.objects.annotate(product_count=Count("product"))
    related_products = Product.objects.filter(category=product.category).exclude(id=pk)[:12]
    vendor = product.vendor

    context = {
        "product": product,
        "vendor": vendor,
        "categories": categories,
        "related_products": related_products,
        "messages": "Product added to cart successfully!",
    }
    return render(request, "ecomm/products.html", context)


def cart(request):
    # if request.user.is_authenticated:
    #     cart, created = Cart.objects.get_or_create(user=request.user)
    #     cart_items = CartItem.objects.filter(cart=cart)
    # else:
    #     cart_items = []

    # context = {
    #     "cart_items": cart_items,
    # }
    return render(request, "ecomm/cart.html")

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Check if the product is already in the user's wishlist
    if Wishlist.objects.filter(user=request.user, product=product).exists():
        messages.info(request, "Product already in your wishlist.")
    else:
        Wishlist.objects.create(user=request.user, product=product)
        messages.success(request, "Product added to your wishlist.")

    return render(request, 'ecomm/products.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product.name} added to cart successfully!")

    # Instead of redirecting, re-render the product page or any page you choose
    return render(request, 'ecomm/product.html', {'product': product})
