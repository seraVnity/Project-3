from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect,  get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Product, Pizza, Topping, Cart, DetailedOrder
# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html", {"message": None})

    pizzas = Product.objects.values(
        'id', 'name', 'type', 'size', 'price', 'pizza__toppings_number')
    context = {
        "user": request.user,
        "toppings": Topping.objects.all(),
        "regular_pizzas": pizzas.filter(type="Pizza Regular"),
        "sicilian_pizzas": pizzas.filter(type="Pizza Sicilian")
    }
    return render(request, "orders/home.html", context)


def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
    else:
        form = UserCreationForm()
    return render(request, 'users/signup.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "users/login.html", {"message": "Invalid credentials."})
    else:
        return render(request, "users/login.html")


def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {"message": "Logged out."})

@login_required
def cart(request):
    if request.method == "GET":
        # products = DetailedOrder.objects.values('product__name','product__size', 'product__type', 'product__price', 'toppings', 'quantity' )

        print(products)
        context = {
            "cart": Cart.objects.all(),
            "orders": DetailedOrder.objects.all()
        }
        return render(request, "orders/cart.html", context)

@login_required
def add_to_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        cart,created = Cart.objects.get_or_create(user=request.user, active = True)
        order,created = DetailedOrder.objects.get_or_create(product=product,cart=cart)
        order.quantity += 1
        order.save()

        toppings = request.POST.getlist('toppings')
        print(toppings)
        if toppings:
            for topping in toppings:
                top = Topping.objects.get(name=topping)
                order.toppings.add(top)

                print(topping, "91")
            print(order.toppings.all())    
        # else:
        #     print("from POST cart view.py file")
        #     order,created = DetailedOrder.objects.get_or_create(product=product,cart=cart)
         
        
        return HttpResponseRedirect(reverse("cart"))

# def add_to_cart(request, product_id):
#     print("Hi from add to cart")
#     product_id = int(product_id)
#     product = get_object_or_404(Product, pk=product_id)
#     print(product, "36")
#     cart,created = Cart.objects.get_or_create(user=request.user, active=True)
#     order,created = DetailedOrder.objects.get_or_create(product=product)
#     order.quantity += 1
#     order.save()
#     messages.success(request, "Cart updated!")
#     return HttpResponse("Hello, world!")
