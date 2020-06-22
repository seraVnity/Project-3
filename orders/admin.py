from django.contrib import admin
from .models import Product, Pizza, Topping, Cart, DetailedOrder

# Register your models here.

class DetailedOrderInline(admin.TabularInline):
    model = DetailedOrder
    extra = 0

class CartAdmin(admin.ModelAdmin):
    inlines = [DetailedOrderInline]

class PizzaInline(admin.TabularInline):
    model = Pizza

class ProductAdmin(admin.ModelAdmin):
    inlines = [PizzaInline]


admin.site.register(Product, ProductAdmin)
admin.site.register(Pizza)
admin.site.register(Cart, CartAdmin)
admin.site.register(DetailedOrder)
admin.site.register(Topping)
