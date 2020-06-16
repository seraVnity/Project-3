from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup", views.signup_view, name="signup"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("cart", views.cart, name="cart"),
    path("cart/<int:product_id>", views.add_to_cart, name="add_to_cart")

]
