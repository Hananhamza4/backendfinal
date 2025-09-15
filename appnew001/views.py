from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import UserProfile
from .models import Product
from .models import CartItem


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        mobile = request.POST['mobile']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error_message': 'Email already exists.'})

        # Create User (username is required in default User model)
        user = User.objects.create_user(username=username, email=email, password=password)

        # Create UserProfile and link it with user
        UserProfile.objects.create(user=user, mobile=mobile)

        login(request, user)
        return redirect('user_login')

    return render(request, 'signup.html')


def user_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            # Get the username linked to this email
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect('indexfun')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid email or password'})

    return render(request, 'login.html')






def newfunc01(request):
    return render(request,"index.html")
# def loginfun(request):
#     return render(request,"login.html")
def indexfun(request):
    return render(request,"index.html")
def error(request):
    return render(request,"404.html")
def about(request):
    return render(request,"about.html")
# def cart(request):
#     return render(request,"cart.html")
def checkout(request):
    return render(request,"checkout.html")
def contact(request):
    return render(request,"contact.html")
def news(request):
    return render(request,"news.html")
def shop(request):
    return render(request,"shop.html")
# def signup(request):
#     return render(request,"signup.html")
def singlen(request):
    return render(request,"single-news.html")
# def singlep(request):
#     return render(request,"single-product.html")

# def product(request):
#     return render(request,'shop.html')


# def singlep(request, id):
#     product = get_list_or_404(Product, id=id)
#     return render(request,'single-product.html', {'product':product})

# def shop(request):
#     products = Product.objects.all()
#     return render(request,"shop.html",{"products":products})
from django.shortcuts import render
from .models import Product

def shop(request):
    products = Product.objects.all()
    return render(request, "shop.html", {"products": products})


def singlep(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, "single-product.html", {"product": product})

# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, CartItem
# @login_required
# def cart(request):
#     cart_items = CartItem.objects.all()
#     cart_total = sum(item.total() for item in cart_items)
#     return render(request, 'cart.html', {'cart_items': cart_items, 'cart_total': cart_total})
@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    subtotal = sum(item.total_price for item in cart_items)  # ← fix here
    shipping = 10 if subtotal > 0 else 0
    total = subtotal + shipping

    return render(request, "cart.html", {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
    })




# @login_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from .models import Product, CartItem

# @login_required
# def add_to_cart(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)
    
#     # Assign the logged-in user
#     cart_item, created = CartItem.objects.get_or_create(
#         product=product,
#         user=request.user  # <-- crucial fix
#     )
    
#     if not created:
#         cart_item.quantity += 1
#         cart_item.save()
    
#     return redirect('cart')
from django.shortcuts import get_object_or_404, redirect
from .models import Product, CartItem
from django.contrib import messages

def add_to_cart(request, product_id):
    # Check if user is authenticated
    if not request.user.is_authenticated:
        # Redirect to login page if not logged in
        return redirect('user_login')
    
    # User is logged in, proceed to add product to cart
    product = get_object_or_404(Product, pk=product_id)
    
    cart_item, created = CartItem.objects.get_or_create(
        product=product,
        user=request.user
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart')
    


# Update quantity in cart
def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()  # if set to 0 → remove item
    return redirect('cart')


# Remove item from cart
def remove_from_cart(request,cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

@login_required
def userprofile(request):
    user = request.user

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        

        # Update user info
        user.username = username
        user.email = email
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("userprofile")

    return render(request, "userprofile.html", {"user": user})

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)  # This clears the session and logs out the user
    return redirect('indexfun')  # 


from .models import UserProfile, Product, CartItem, BillingDetails, Order, OrderItem, Contact
from .forms import BillingDetailsForm
# Checkout
@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.warning(request, "Your cart is empty!")
        return redirect('cart')

    subtotal = sum(item.total_price for item in cart_items)
    shipping = 10 if subtotal > 0 else 0
    total = subtotal + shipping

    billing_details = BillingDetails.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = BillingDetailsForm(request.POST, instance=billing_details)
        if form.is_valid():
            billing = form.save(commit=False)
            billing.user = request.user
            billing.save()

            # Create Order
            order = Order.objects.create(
                user=request.user,
                total_amount=total,
                total_quantity=sum(item.quantity for item in cart_items),
                shipping_address=billing.address
            )

            # Create OrderItems
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            # Clear cart
            cart_items.delete()
            messages.success(request, "Order placed successfully!")
            return redirect('order_summary', order_id=order.id)
    else:
        form = BillingDetailsForm(instance=billing_details)

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
        'form': form
    })
from django.contrib import messages


@login_required
def order_summary(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "order_summary.html", {"order": order})

#chatgpt  

def order_summary(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    items = order.items.all()

    subtotal = 0
    for item in items:
        item.subtotal = item.quantity * item.price
        subtotal += item.subtotal

    return render(request, "order_summary.html", {
        "order": order,
        "items": items,
        "subtotal": subtotal,
    })


import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Order  # Adjust the import based on your project structure



# Initialize Razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@csrf_exempt
def razorpay_payment(request, order_id):
    if request.method == 'POST':
        try:
            order = Order.objects.get(id=order_id)
            total_price = order.total_amount  # make sure field name matches model

            amount_in_paise = int(total_price * 100)

            razorpay_order = client.order.create({
                "amount": amount_in_paise,
                "currency": "INR",
                "payment_capture": 1
            })

            order.razorpay_order_id = razorpay_order['id']
            order.save()

            return JsonResponse({
                'razorpay_order_id': razorpay_order['id'],
                'razorpay_key_id': settings.RAZORPAY_KEY_ID,
                'amount': amount_in_paise,
                'currency': "INR"
            })

        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)
