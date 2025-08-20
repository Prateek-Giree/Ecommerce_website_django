from .models import (
    Category,
    Product,
    Cart,
    CartItem,
    Wishlist,
    DeliveryAddress,
    UserProfile,
    PasswordResetOTP,
)
from django.db.models import Count
from .models import Order, OrderItem, CartItem
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .quick_sort import quicksort_products
from .searching_algo import linear_search_partial
from django.db.models import Sum, Count,F,FloatField
from django.db.models.functions import TruncMonth
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import base64, hmac, hashlib
import json
from django.utils.dateparse import parse_date


# =============================================================
def about(request):
    return render(request, "ecomm/about_us.html")

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()

        # Basic validation
        if all([name, email, message]):
            send_mail(
                subject=f"FastCart contact form - from {name}",
                message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
                from_email=email,
                recipient_list=["fastcart.onlineshop@gmail.com"],
                fail_silently=False,
            )
            messages.success(request, "Message sent!")
            return redirect("contact")
        else:
            messages.error(request, "Please fill in all fields.")

    return render(request, "ecomm/about_us.html")
# =============================================================


def register(request):

    if request.user.is_authenticated:
        return redirect("index")

    delivery_addresses = DeliveryAddress.objects.all()
    # get form data
    if request.method == "POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        delivery_addr_id = request.POST.get("delivery_addr")
        password = request.POST.get("pass")
        cpass = request.POST.get("cpass")

        # print(fullname,email,phone,address,delivery_addr_id,password,cpass)
        if password != cpass:
            messages.error(request, "Password do not match")
            return redirect("register")

        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered")
            return redirect("register")


        username = email.split("@")[0]
        user = User.objects.create(
            username=username,
            email=email,
            first_name=fullname,
            password=make_password(password),
        )

        # Create UserProfile
        delivery_address = DeliveryAddress.objects.get(id=delivery_addr_id)
        UserProfile.objects.create(
            user=user, phone=phone, address=address, delivery_address=delivery_address
        )

        messages.success(request, "Registration successful! Please log in.")
        return redirect("login")

    page = "register"
    context = {
        "page": page,
        "delivery_addresses": delivery_addresses,
    }
    return render(request, "ecomm/login_register.html", context)


# =============================================================


def login_view(request):

    # Check if the user is already logged in
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("pass")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=email, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, "Login successful!")
                return redirect("index")
            else:
                messages.error(request, "Invalid password")
        except User.DoesNotExist:
            messages.error(request, "User does not exist")

    page = "login"

    context = {
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
    related_products = Product.objects.filter(category=product.category).exclude(id=pk)[
        :12
    ]
    vendor = product.vendor

    context = {
        "product": product,
        "vendor": vendor,
        "categories": categories,
        "related_products": related_products,
    }
    return render(request, "ecomm/products.html", context)


# =============================================================


@login_required(login_url="login")
def profile(request, pk):

    # Get the user profile
    user = get_object_or_404(User, id=pk)
    user_profile = get_object_or_404(UserProfile, user=user)
    delivery_address = user_profile.delivery_address

    # Get the user's wishlist
    wishlist = Wishlist.objects.filter(user=user)

    # Get the user's cart
    cart, created = Cart.objects.get_or_create(user=user)
    cart_items = CartItem.objects.filter(cart=cart)

    # Get users order
    order_items = OrderItem.objects.filter(order__user=user)
    order_item_count = order_items.count()

    context = {
        "user": user,
        "user_profile": user_profile,
        "delivery_address": delivery_address,
        "wishlist": wishlist,
        "cart_items": cart_items,
        "order_item_count": order_item_count,
    }
    return render(request, "ecomm/profile.html", context)


# =============================================================


@login_required(login_url="login")
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
                pass
        if request.FILES.get("profile_image"):
            user_profile.profile_image = request.FILES["profile_image"]

        user_profile.save()

        messages.success(request, "Profile updated successfully.")
        return redirect("profile", pk=user.id)

    delivery_addresses = DeliveryAddress.objects.all()
    wishlist = Wishlist.objects.filter(user=user)
    cart, _ = Cart.objects.get_or_create(user=user)
    cart_items = CartItem.objects.filter(cart=cart)
    order_items = OrderItem.objects.filter(order__user=user)
    order_item_count = order_items.count()

    # Change password
    if request.method == "POST" and "change_password" in request.POST:
        current_password = request.POST.get("currentPassword")
        new_password = request.POST.get("newPassword")
        confirm_new_password = request.POST.get("confirmPassword")

        if not check_password(current_password, user.password):
            messages.error(request, "Current password is incorrect.")
        elif new_password == current_password:
            messages.error(
                request, "New password cannot be the same as the current password."
            )
        elif len(new_password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
        elif new_password != confirm_new_password:
            messages.error(request, "New passwords do not match.")
        else:
            user.password = make_password(new_password)
            user.save()
            logout(request)  # Terminates the session
            messages.success(
                request, "Password changed successfully. Please log in again."
            )
            return redirect("login")

    context = {
        "user": user,
        "user_profile": user_profile,
        "delivery_address": user_profile.delivery_address,
        "wishlist": wishlist,
        "cart_items": cart_items,
        "delivery_addresses": delivery_addresses,
        "order_item_count": order_item_count,
    }

    return render(request, "ecomm/edit_profile.html", context)


# =============================================================


@login_required(login_url="login")
def cart(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be logged in to view your cart.")
        return render(request, "ecomm/cart.html")

    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.select_related("product")
    cart_items = CartItem.objects.filter(cart=cart)

    context = {
        "cart": cart,
        "items": items,
        "cart_items": cart_items,
        "total": cart.total_price(),
    }
    return render(request, "ecomm/cart.html", context)


# =============================================================


@login_required(login_url="login")
def remove_from_cart(request, pk):
    if not request.user.is_authenticated:
        messages.error(
            request, "You need to be logged in to remove items from your cart."
        )
        return redirect("cart")

    cart = get_object_or_404(Cart, user=request.user)
    try:
        item = CartItem.objects.get(id=pk, cart=cart)
        item.delete()
        messages.success(request, "Item removed from cart successfully.")
    except CartItem.DoesNotExist:
        messages.error(request, "Item not found in your cart.")

    return redirect("cart")


# =============================================================


@login_required(login_url="login")
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    try:
        qty = int(request.POST.get("qty", 1))
        if qty < 1:
            qty = 1
    except ValueError:
        qty = 1

    if product.stock == 0:
        messages.error(request, f"Sorry, {product.name} is out of stock.")
        return redirect(request.META.get("HTTP_REFERER", "index"))

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    existing_qty = cart_item.quantity if not created else 0
    new_total_qty = existing_qty + qty

    if new_total_qty > product.stock:
        qty_to_add = product.stock - existing_qty
        if qty_to_add > 0:
            cart_item.quantity = existing_qty + qty_to_add
            cart_item.save()
            messages.warning(
                request,
                f"Only {qty_to_add} more items of {product.name} were added. Stock limit reached.",
            )
        else:
            messages.error(
                request,
                f"Cannot add more of {product.name}. You've already added the maximum stock available.",
            )
    else:
        cart_item.quantity = new_total_qty
        cart_item.save()
        messages.success(
            request, f"{product.name} added to cart (×{qty}) successfully!"
        )

    return redirect(request.META.get("HTTP_REFERER", "index"))


# =============================================================


@login_required(login_url="login")
def clear_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        CartItem.objects.filter(cart=cart).delete()
        messages.success(request, "Your cart has been cleared.")
    else:
        messages.info(request, "Your cart is already empty.")

    return redirect("cart")


# =============================================================


@login_required(login_url="login")
@require_POST
def update_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    updated = False

    for item in cart.items.all():
        input_name = f"quantity_{item.id}"
        new_qty = request.POST.get(input_name)

        try:
            new_qty = int(new_qty)
            if new_qty < 1:
                new_qty = 1
            elif new_qty > item.product.stock:
                new_qty = item.product.stock

            if item.quantity != new_qty:
                item.quantity = new_qty
                item.save()
                updated = True
        except (ValueError, TypeError):
            continue

    if updated:
        messages.success(request, "Cart updated successfully.")
    else:
        messages.info(request, "No changes were made to your cart.")

    return redirect("cart")


# =============================================================


def category_page(request, pk):
    categories = Category.objects.filter(id=pk)
    category_products = {
        category: Product.objects.filter(category=category) for category in categories
    }
    context = {"category_products": category_products}
    return render(request, "ecomm/category_page.html", context)


# =============================================================


@login_required(login_url="login")
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user, product=product
    )

    if created:
        messages.success(request, f"{product.name} added to wishlist successfully!")
    else:
        messages.info(request, f" {product.name} is already in your wishlist.")

    return redirect(request.META.get("HTTP_REFERER", "index"))

# =============================================================

@login_required(login_url="login")
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    messages.success(request, f"{product.name} removed from wishlist successfully!")

    return redirect("wishlist")

# =============================================================

@login_required(login_url="login")
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related(
        "product"
    )
    return render(request, "ecomm/wishlist.html", {"wishlist_items": wishlist_items})


# =============================================================


@login_required(login_url="login")
def view_order(request):
    orders = (
        Order.objects.filter(user=request.user)
        .prefetch_related("items", "items__product")
        .order_by("-date_ordered")
    )

    context = {
        "orders": orders,
    }
    return render(request, "ecomm/order.html", context)
# =============================================================

@login_required(login_url="login")
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status == "Pending":
        with transaction.atomic():
            for item in order.items.all():
                product = item.product
                product.stock += item.quantity
                product.save()
            order.delete()
        messages.success(request, "Your order has been cancelled")
    else:
        messages.error(request, "Only pending orders can be cancelled.")

    return redirect("view_order")
# =============================================================

def generate_signature(payload, secret):
    message = json.dumps(payload, separators=(',', ':'))
    signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()
    return base64.b64encode(signature).decode()

# =============================================================

@login_required(login_url="login")
def checkout_view(request):
    user = request.user

    try:
        cart = Cart.objects.get(user=user)
        profile = UserProfile.objects.get(user=user)
    except ObjectDoesNotExist:
        messages.error(request, "Cart or user profile not found.")
        return redirect("cart")

    if request.method == "POST":
        action_type = request.POST.get("action_type")

        # Step 1: Save selected items
        if action_type == "proceed_to_checkout":
            selected_ids = request.POST.getlist("selected_items")
            if not selected_ids:
                messages.error(request, "No items selected for checkout.")
                return redirect("cart")
            request.session["checkout_selected_ids"] = selected_ids
            return redirect("checkout")

        # Step 2: Place order (COD or eSewa)
        elif action_type == "place_order":
            payment_method = "cod" if request.POST.get("cod") == "cod" else "esewa" if request.POST.get("esewa") == "esewa" else None
            if not payment_method:
                messages.error(request, "Invalid payment method.")
                return redirect("checkout")

            selected_ids = request.session.get("checkout_selected_ids", [])
            cart_items = cart.items.filter(id__in=selected_ids)
            if not cart_items.exists():
                messages.error(request, "No valid items in cart to place order.")
                return redirect("cart")

            total_price = sum(
                (item.product.new_price or item.product.price) * item.quantity
                for item in cart_items
            )

            # Create Order and OrderItems
            with transaction.atomic():
                order = Order.objects.create(
                    user=user,
                    name=user.get_full_name() or user.username,
                    address=profile.address,
                    total_price=total_price,
                    status="Pending"
                )

                for item in cart_items:
                    if payment_method == "cod" and item.quantity > item.product.stock:
                        messages.error(request, f"Insufficient stock for {item.product.name}.")
                        return redirect("checkout")

                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.get_total_price()
                    )

                    if payment_method == "cod":
                        item.product.stock -= item.quantity
                        item.product.save()

            # COD: finalize order
            if payment_method == "cod":
                cart_items.delete()
                del request.session["checkout_selected_ids"]
                messages.success(request, "Order placed successfully!")
                return redirect("index")

            # eSewa: prepare payment form
            transaction_uuid = order.transaction_uuid
            product_code = "EPAYTEST"
            signed_field_names = "total_amount,transaction_uuid,product_code"
            signed_string = f"total_amount={total_price},transaction_uuid={transaction_uuid},product_code={product_code}"
            secret_key = "8gBm/:&EnhH.1/q".encode("utf-8")
            signature = base64.b64encode(
                hmac.new(secret_key, signed_string.encode("utf-8"), hashlib.sha256).digest()
            ).decode("utf-8")
            success_url = f"http://127.0.0.1:8000/esewa/success/"
            failure_url = "http://127.0.0.1:8000/esewa/failure/"
            context = {
                "amount": str(total_price),
                "tax_amount": "0",
                "total_amount": str(total_price),
                "transaction_uuid": transaction_uuid,
                "product_code": product_code,
                "product_service_charge": "0",
                "product_delivery_charge": "0",
                "signed_field_names": signed_field_names,
                "signature": signature,
                 "success_url": success_url,
                "failure_url": failure_url,
                
            }
            return render(request, "ecomm/esewa_redirect.html", context)

    # GET request → Show checkout page
    selected_ids = request.session.get("checkout_selected_ids", [])
    if not selected_ids:
        messages.error(request, "No items selected for checkout.")
        return redirect("cart")

    cart_items = cart.items.filter(id__in=selected_ids)
    cart.total_price = sum(
        (item.product.new_price or item.product.price) * item.quantity
        for item in cart_items
    )

    return render(request, "ecomm/checkout.html", {
        "user": user,
        "profile": profile,
        "cart": cart,
        "cart_items": cart_items,
        "selected_ids": selected_ids,
    })
# =============================================================


import requests


@login_required(login_url="login")
def esewa_success(request):
    user = request.user

    # Get encoded data from query params
    encoded_data = request.GET.get("data")
    if not encoded_data:
        messages.error(request, "Missing payment data.")
        return redirect("checkout")

    # Decode Base64 -> JSON
    try:
        decoded_bytes = base64.b64decode(encoded_data)
        decoded_str = decoded_bytes.decode("utf-8")
        decoded_data = json.loads(decoded_str)
    except Exception as e:
        messages.error(request, f"Failed to decode payment data: {str(e)}")
        return redirect("checkout")

    # Extract transaction details
    transaction_uuid = decoded_data.get("transaction_uuid")
    total_amount = decoded_data.get("total_amount")

    print("Transaction UUID (from decoded data):", transaction_uuid)
    print("Total Amount (from decoded data):", total_amount)

    if not transaction_uuid or not total_amount:
        messages.error(request, "Invalid payment details.")
        return redirect("checkout")

    # Get the unpaid order using transaction_uuid (instead of order_id)
    order = get_object_or_404(Order, transaction_uuid=transaction_uuid, user=user, is_paid=False)

    # Verify payment with eSewa
    status_url = "https://rc.esewa.com.np/api/epay/transaction/status/"
    params = {
        "product_code": "EPAYTEST",
        "transaction_uuid": transaction_uuid,
        "total_amount": total_amount,
    }

    try:
        response = requests.get(status_url, params=params, timeout=10)
        response.raise_for_status()
        status_data = response.json()
    except requests.RequestException as e:
        messages.error(request, f"Payment verification failed: {str(e)}")
        return redirect("checkout")
    except ValueError:
        messages.error(request, "Invalid response from eSewa.")
        return redirect("checkout")

    # Check payment status
    if status_data.get("status") == "COMPLETE":
        with transaction.atomic():
            order.is_paid = True
            order.status = "Pending"
            order.save()

            # Remove purchased items from cart
            try:
                cart = Cart.objects.get(user=user)
                selected_ids = request.session.get("checkout_selected_ids", [])
                if selected_ids:
                    cart.items.filter(id__in=selected_ids).delete()
                    del request.session["checkout_selected_ids"]
            except Cart.DoesNotExist:
                pass

            # Deduct stock for each product
            for item in order.items.all():
                item.product.stock -= item.quantity
                item.product.save()


        messages.success(request, f"Payment successful! Ref ID: {status_data.get('ref_id')}")
        return redirect("index")

    else:
        messages.error(request, "Payment failed or pending. Please try again.")
        return redirect("checkout")


@csrf_exempt
def esewa_failure(request):
    messages.error(request, "Payment failed or canceled.")
    return redirect('checkout')

# =============================================================




def forgot_password_request(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "No user found with this email.")
            return redirect('forgot_password')

        # Generate 6 digit OTP
        otp = str(random.randint(100000, 999999))
        # Save OTP to DB
        PasswordResetOTP.objects.create(user=user, otp=otp)

        send_mail(
        subject='FastCart Password Reset OTP',
        message=(
                f"Dear User,\n\n"
                f"We received a request to reset your password for your FastCart account.\n\n"
                f"Your One-Time Password (OTP) is: {otp}\n"
                f"This OTP is valid for 10 minutes.\n\n"
                f"If you did not request a password reset, please ignore this email.\n\n"
                f"Regards,\n"
                f"The FastCart Team"
            ),
        from_email='FastCart <fastcart.onlineshop@gmail.com>',
        recipient_list=[email],
        fail_silently=False,
        )

        request.session['reset_email'] = email  # Save email in session for verification step
        messages.success(request, "OTP sent to your email.")
        return redirect('verify_otp')

    return render(request, 'account/forgot_password.html')
# =============================================================

def verify_otp(request):
    if request.method == "POST":
        otp_input = request.POST.get('otp')
        email = request.session.get('reset_email')

        if not email:
            messages.error(request, "Session expired. Please try again.")
            return redirect('forgot_password')

        try:
            user = User.objects.get(email=email)
            otp_obj = PasswordResetOTP.objects.filter(user=user, is_verified=False).latest('created_at')
        except (User.DoesNotExist, PasswordResetOTP.DoesNotExist):
            messages.error(request, "Invalid request. Please try again.")
            return redirect('forgot_password')

        if otp_obj.is_expired():
            messages.error(request, "OTP expired. Please request a new one.")
            otp_obj.delete()
            return redirect('forgot_password')

        if otp_obj.otp == otp_input:
            otp_obj.is_verified = True
            otp_obj.save()
            request.session['otp_verified_email'] = email  # Mark verified session for password reset
            messages.success(request, "OTP verified. You can now reset your password.")
            return redirect('reset_password')
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect('verify_otp')
    
    return render(request, 'account/verify_otp.html')
# =============================================================

def reset_password(request):
    email = request.session.get('otp_verified_email')
    if not email:
        messages.error(request, "Unauthorized access.")
        return redirect('forgot_password')

    if request.method == "POST":
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('reset_password')

        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()

        # Clean up session
        del request.session['reset_email']
        del request.session['otp_verified_email']

        messages.success(request, "Password reset successful. You can now login.")
        return redirect('login')

    return render(request, 'account/password_reset.html')




def product_filter(request):
    products = list(Product.objects.all())
    categories = Category.objects.all()

    category = request.GET.get('filterBy')
    sort_by = request.GET.get('sortBy')

    if category:
        products = [p for p in products if p.category.name.lower() == category.lower()]

    if sort_by == 'name':
        products = quicksort_products(products, key_func=lambda p: p.name.lower())
    elif sort_by == 'category':
        products = quicksort_products(products, key_func=lambda p: p.category.name.lower())
    elif sort_by == 'price-asc':
        products = quicksort_products(products, key_func=lambda p: p.new_price if p.new_price is not None else p.price)
    elif sort_by == 'price-desc':
        products = quicksort_products(products, key_func=lambda p: p.new_price if p.new_price is not None else p.price, reverse=True)
    elif sort_by == 'id':
        products = quicksort_products(products, key_func=lambda p: p.id)

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 10)  # Show 10 products per page

    try:
        paginated_products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        paginated_products = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page of results.
        paginated_products = paginator.page(paginator.num_pages)

    context = {
        'products': paginated_products,
        'results_count': len(products),
        'categories': categories,
        'paginator': paginator,
        'page_obj': paginated_products,
    }
    return render(request, 'ecomm/filter_search.html', context)



def category_filter(request):
    selected_category_id = request.GET.get("category")
    categories = Category.objects.order_by('name')

    if selected_category_id:
        products = Product.objects.filter(category__id=selected_category_id)
        current_category = Category.objects.filter(id=selected_category_id).first()
    else:
        products = Product.objects.all()
        current_category = None

    context = {
        'categories': categories,
        'products': products,
        'current_category': current_category
    }
    return render(request, "ecomm/category_filter.html", context)

def product_search(request):
    query = request.GET.get("q", "").strip()
    product_list = Product.objects.all()
    product_list = list(product_list)  # convert queryset to list

    results = linear_search_partial(product_list, query) if query else []

    context = {
        "query": query,
        "results": results,
    }

    if query:
        if results:
            messages.success(request, f"{len(results)} result(s) found for '{query}'")
        else:
            messages.warning(request, f"No product found for '{query}'")

    return render(request, "ecomm/search_product.html", context)



User = get_user_model()
@staff_member_required
def analytics_view(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    order_filter = {}
    user_filter = {}

    if start_date:
        order_filter["date_ordered__gte"] = parse_date(start_date)
        user_filter["date_joined__gte"] = parse_date(start_date)

    if end_date:
        order_filter["date_ordered__lte"] = parse_date(end_date)
        user_filter["date_joined__lte"] = parse_date(end_date)

    # Apply filters
    filtered_orders = Order.objects.filter(**order_filter)
    filtered_users = User.objects.filter(**user_filter)

    # -------- NON-DATE-BASED STATS --------
    products_per_category = Product.objects.values('category__name').annotate(
        product_count=Count('id')
    ).order_by('category__name')

    stock_per_category = Product.objects.values('category__name').annotate(
        total_stock=Sum('stock')
    ).order_by('category__name')

    low_stock_products = Product.objects.filter(stock__lt=10).order_by('stock')

    # -------- DATE-BASED SALES STATS --------
    sales_per_category = (
        OrderItem.objects.filter(order__in=filtered_orders)
        .values('product__category__name')
        .annotate(
            total_revenue=Sum(F('price') * F('quantity'), output_field=FloatField())
        )
        .order_by('product__category__name')
    )

    sales_over_time = (
        filtered_orders.annotate(month=TruncMonth('date_ordered'))
        .values('month')
        .annotate(total_sales=Sum('total_price'))
        .order_by('month')
    )

    top_products_sold = (
        OrderItem.objects.filter(order__in=filtered_orders)
        .values('product__name')
        .annotate(total_sold=Sum('quantity'))
        .order_by('-total_sold')[:5]
    )

    users_per_month = (
        filtered_users.annotate(month=TruncMonth('date_joined'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    context = {
        'products_per_category': products_per_category,
        'sales_per_category': sales_per_category,
        'stock_per_category': stock_per_category,
        'users_per_month': users_per_month,
        'sales_over_time': sales_over_time,
        'top_products_sold': top_products_sold,
        'low_stock_products': low_stock_products,
        'total_products': Product.objects.count(),
        'total_users': filtered_users.count(),
        'total_orders': filtered_orders.count(),
        'total_category': Category.objects.count(),
    }
    return render(request, 'analytics/analytics.html', context)