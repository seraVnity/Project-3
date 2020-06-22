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

    products = Product.objects.all()

    cart = get_or_none(Cart, user=request.user, active=True)
    orders = DetailedOrder.objects.filter(cart=cart)
    counter = 0
    if orders:
        for order in orders:
            counter += order.quantity

    context = {
        "user": request.user,
        "toppings": Topping.objects.all(),
        "regular_pizzas": pizzas.filter(type="Pizza Regular"),
        "sicilian_pizzas": pizzas.filter(type="Pizza Sicilian").order_by('name'),
        "subs": pizzas.filter(type="Sub"),
        "pastas": pizzas.filter(type="Pasta"),
        "salads": pizzas.filter(type="Salad"),

        "counter": counter
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
        cart = get_or_none(Cart, user=request.user, active=True)
        orders = DetailedOrder.objects.filter(cart=cart)
        print("----from CART---", "cart", cart, "order", orders)
        if cart:
            total = 0
            for order in orders:
                if order.quantity == 0:
                    total += order.product.price
                else:
                    sum = order.product.price * order.quantity
                    total += sum
            cart.total = round(total, 2)
            cart.save()
        context = {
            "cart": cart,
            "orders": orders,
        }
        return render(request, "orders/cart.html", context)


@login_required
def add_to_cart(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(
            user=request.user, active=True)

        toppings = request.POST.getlist('toppings')
        if toppings:
            # check there is no such products with these toppings in the order
            orders = get_or_none(DetailedOrder, product=product)
            if orders:
                print(orders, "----orders----")
                for exist_order in orders:
                    list = exist_order.toList()
                    # if this topping list already exists in orders increase order quantity
                    if list == toppings:
                        exist_order.quantity += 1
                        exist_order.save()
                        return HttpResponseRedirect(reverse("cart"))

            new_order = DetailedOrder.objects.create(
                product=product, cart=cart)
            for topping in toppings:
                top = Topping.objects.get(name=topping)
                new_order.toppings.add(top)
            new_order.quantity += 1
            new_order.save()

        else:
            order, created = DetailedOrder.objects.get_or_create(
                product=product, cart=cart)
            order.quantity += 1
            order.save()

        return HttpResponseRedirect(reverse("index"))

@login_required
def remove_from_cart(request, order_id):
    order = get_object_or_404(DetailedOrder, id=order_id)
    print(order)
    if order.quantity == 1:
        order.delete()
        print("----quantity == 1, from remove cart")

    else:
        order.quantity -= 1
        order.save()
        print(order, "----from remove cart")

    return HttpResponseRedirect(reverse("cart"))

def confirm_order(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id, active=True)
    cart.active = False
    cart.placed = True
    cart.save()
    context = {
        "cart": cart
    }
    return render(request, "orders/confirm.html", context)

def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None

