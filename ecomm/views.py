from .models import Category, Product,Cart, CartItem,Wishlist,DeliveryAddress,UserProfile
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login as auth_login




def register(request):
   
    delivery_addresses= DeliveryAddress.objects.all()
    #get form data
    if request.method == "POST":
        fullname=request.POST.get("fullname")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        address=request.POST.get("address")
        delivery_addr_id=request.POST.get("delivery_addr")
        password=request.POST.get("pass")
        cpass=request.POST.get("cpass")
        
        print(fullname,email,phone,address,delivery_addr_id,password,cpass)
        if password != cpass:
            messages.error(request, "Password do not match")
            return redirect('register')
        
        # Email already registered?
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered")
            return redirect('register')

        # Create User
        username = email.split("@")[0]  # or use custom logic
        user = User.objects.create(
            username=username,
            email=email,
            first_name=fullname,
            password=make_password(password)
        )

        # Create UserProfile
        delivery_address = DeliveryAddress.objects.get(id=delivery_addr_id)
        UserProfile.objects.create(
            user=user,
            phone=phone,
            address=address,
            delivery_address=delivery_address
        )

        messages.success(request, "Registration successful! Please log in.")
        return redirect('login')
        

    page="register"
    context={
        "page": page,
        "delivery_addresses": delivery_addresses,
    }
    return render(request, "ecomm/login_register.html",context)

def login_view(request):
    
    # Check if the user is already logged in
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("pass")  # 'password', not 'pass'

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=email, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, "Login successful!")
                return redirect('index')
            else:
                messages.error(request, "Invalid password")
        except User.DoesNotExist:
            messages.error(request, "User does not exist")   
             
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
