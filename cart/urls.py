from django.urls import path

from cart.controller.cart_controller import CartController

urlpatterns = [
    path('cart', CartController.as_view()),
]
