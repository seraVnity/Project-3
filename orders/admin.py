from django.contrib import admin
from .models import Product, Pizza, Sub, DinnerPlates, Topping

# Register your models here.
admin.site.register(Product)
admin.site.register(Pizza)
admin.site.register(Sub)
admin.site.register(DinnerPlates)
admin.site.register(Topping)

