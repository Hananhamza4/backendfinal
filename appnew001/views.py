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

def cart(request):
    cart_items = CartItem.objects.all()  # or filter(user=request.user) if per-user
    subtotal = sum(item.total() for item in cart_items)
    shipping = 10 if subtotal > 0 else 0  # example flat rate shipping
    total = subtotal + shipping

    return render(request, "cart.html", {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
    })


# @login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product)
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












# Create your views here.
