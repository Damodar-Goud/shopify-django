from django.urls import path

from .views import (
    CartAddView,
    CartView,
    CartUpdateView,
    CartRemoveView,
    CheckoutView,
    OrderListView,
)

urlpatterns = [
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/update/", CartUpdateView.as_view(), name="cart-update"),
    path("cart/remove/", CartRemoveView.as_view(), name="cart-remove"),
    path("cart/add/", CartAddView.as_view(), name="cart-add"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("", OrderListView.as_view(), name="order-list"),
]
