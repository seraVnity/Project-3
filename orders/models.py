from django.db import models
from django import forms
from django.conf import settings

# Create your models here.
class Product(models.Model):
    NULL = 'None'
    SM = 'Small'
    LG = 'Large'
    SIZE = [(NULL, 'None'), (SM, 'Small'), (LG, 'Large')]

    size = models.CharField(max_length=6, choices=SIZE, default=NULL)
    name = models.CharField(max_length=64)
    type = models.CharField(max_length=64)
    price = models.FloatField()

    def __str__(self):
        return f"{self.size} {self.type} '{self.name}' costs {self.price}"

class Topping(models.Model):
    name = models.CharField(max_length=64, null=True)

    def __str__(self):
        return f"{self.name}"

class Pizza(models.Model):
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FIVE = 5
    TOPPINGS_NUMBER = [(ZERO, 0),
                       (ONE, 1),
                       (TWO, 2),
                       (THREE, 3),
                       (FIVE, 5)]

    product = models.OneToOneField(Product, on_delete=models.CASCADE,
        primary_key=True,)
    toppings_number = models.IntegerField(
        choices=TOPPINGS_NUMBER, default=ZERO)

    def __str__(self):
        return f"{self.toppings_number}"


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,)
    order_date = models.DateTimeField(auto_now_add=True, null=True)
    active = models.BooleanField(default=False)
    placed = models.BooleanField(default=False)
    total = models.FloatField(default=0)

    def __str__(self):
        if self.placed:
            return f"Placed Order N{self.id} of {self.user}"
        else:
            return f"Active Order N{self.id} of {self.user} was created on {self.order_date}"

class DetailedOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default = 0)
    toppings = models.ManyToManyField(Topping)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.quantity} {self.product} has {self.toppings.count()} toppings cart N{self.cart.id}"
    
    def toList(self):
        list = []
        for topping in self.toppings.all():
            list.append(topping.name)
        return list



