from django.contrib import admin
from .models import Product, Pizza, Topping, Cart, DetailedOrder

# Register your models here.
admin.site.register(Product)
admin.site.register(Pizza)
admin.site.register(Cart)
admin.site.register(DetailedOrder)
admin.site.register(Topping)

