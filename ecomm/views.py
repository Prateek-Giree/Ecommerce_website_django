from .models import Category, Product,Cart, CartItem,Wishlist,DeliveryAddress,UserProfile
from django.db.models import Count
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404, render,redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

# =============================================================
@staff_member_required
def analytics_view(request):
    # Prepare data for charts (e.g., order stats, product sales, etc.)
    return render(request, "ecomm/analytics.html")

# =============================================================
def about(request):
    return render(request,"ecomm/about_us.html")


# =============================================================

def register(request):

    if request.user.is_authenticated:
        return redirect('index')
   
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


# =============================================================

def login_view(request):
    
    # Check if the user is already logged in
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("pass")

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


# =============================================================

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


# =============================================================

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
    }
    return render(request, "ecomm/products.html", context)


# =============================================================

@login_required(login_url='login')
def profile(request,pk):
    
    # Get the user profile
    user = get_object_or_404(User, id=pk)
    user_profile = get_object_or_404(UserProfile, user=user)
    delivery_address = user_profile.delivery_address

    # Get the user's wishlist
    wishlist = Wishlist.objects.filter(user=user)

    # Get the user's cart
    cart, created = Cart.objects.get_or_create(user=user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    context={
        "user": user,
        "user_profile": user_profile,
        "delivery_address": delivery_address,
        "wishlist": wishlist,
        "cart_items": cart_items,
    }
    return render(request, "ecomm/profile.html",context)


# =============================================================

@login_required(login_url='login')
def edit_profile(request):
    user = get_object_or_404(User, id=request.user.id)
    user_profile = get_object_or_404(UserProfile, user=user)

    # Edit personal information
    if request.method == "POST" and "update_details" in request.POST:
        full_name = request.POST.get("fullName", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        primary_address = request.POST.get("address", "").strip()
        delivery_address_id = request.POST.get("delivery_addr")

        user.first_name = full_name
        user.email = email
        user.save()

        user_profile.phone = phone
        user_profile.address = primary_address

        if delivery_address_id:
            try:
                delivery_address = DeliveryAddress.objects.get(id=delivery_address_id)
                user_profile.delivery_address = delivery_address
            except DeliveryAddress.DoesNotExist:
                pass  # optionally log or handle error

        user_profile.save()

        messages.success(request, "Profile updated successfully.")
        return redirect("profile", pk=user.id)

    delivery_addresses = DeliveryAddress.objects.all()
    wishlist = Wishlist.objects.filter(user=user)
    cart, _ = Cart.objects.get_or_create(user=user)
    cart_items = CartItem.objects.filter(cart=cart)

    # Change password
    if request.method == "POST" and "change_password" in request.POST:
        current_password = request.POST.get("currentPassword")
        new_password = request.POST.get("newPassword")
        confirm_new_password = request.POST.get("confirmPassword")

        if not check_password(current_password, user.password):
           messages.error(request, "Current password is incorrect.")
        elif new_password == current_password:
            messages.error(request, "New password cannot be the same as the current password.")
        elif len(new_password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
        elif new_password != confirm_new_password:
            messages.error(request, "New passwords do not match.")
        else:
            user.password = make_password(new_password)
            user.save()
            logout(request)  # Terminates the session
            messages.success(request, "Password changed successfully. Please log in again.")
            return redirect("login")
    
    context = {
        "user": user,
        "user_profile": user_profile,
        "delivery_address": user_profile.delivery_address,
        "wishlist": wishlist,
        "cart_items": cart_items,
        "delivery_addresses": delivery_addresses,
    }

    return render(request, "ecomm/edit_profile.html", context)




# =============================================================

@login_required(login_url='login')
def cart(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to view your cart.")
        return render(request, "ecomm/cart.html")  # or redirect to login

    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.select_related('product')  # efficient query

    context = {
        'cart': cart,
        'items': items,
        'total': cart.total_price(),
    }
    return render(request, "ecomm/cart.html", context)


# =============================================================

@login_required
def remove_from_cart(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to remove items from your cart.")
        return redirect('cart')

    cart = get_object_or_404(Cart, user=request.user)
    try:
        item = CartItem.objects.get(id=pk, cart=cart)
        item.delete()
        messages.success(request, "Item removed from cart successfully.")
    except CartItem.DoesNotExist:
        messages.error(request, "Item not found in your cart.")

    return redirect('cart')

# =============================================================

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{product.name} added to cart successfully!")

    # re-rendering the product page 
    return render(request, 'ecomm/product.html', {'product': product})

# =============================================================

def category_page(request,pk):
     # Fetch all categories
    categories = Category.objects.filter(id=pk)

    # Create a dictionary with category and its products
    category_products = {
        category: Product.objects.filter(category=category)
        for category in categories
    }

    context={
        "category_products": category_products
    }
    return render(request, "ecomm/category_page.html", context)

# =============================================================

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

    if created:
        messages.success(request, f"{product.name} added to wishlist successfully!")
    else:
        messages.info(request, f" {product.name} is already in your wishlist.")

    return redirect(request.META.get('HTTP_REFERER', 'index'))


@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    messages.success(request, f"{product.name} removed from wishlist successfully!")

    return redirect('wishlist')


@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'ecomm/wishlist.html', {'wishlist_items': wishlist_items})
# =============================================================
