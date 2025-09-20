from django.urls import path

from .views import (
    CartAddView,
    CartView,
    CartUpdateView,
    CartRemoveView,
    CheckoutView,
    OrderListView,
    OrderStatusUpdateView,
)

urlpatterns = [
    path("cart/", CartView.as_view(), name="cart"),
    # path("cart/update/", CartUpdateView.as_view(), name="cart-update"),
    # path("cart/remove/", CartRemoveView.as_view(), name="cart-remove"),
    path(
        "cart/item/<int:item_id>/update/",
        CartUpdateView.as_view(),
        name="cart-item-update",
    ),
    path(
        "cart/item/<int:item_id>/remove/",
        CartRemoveView.as_view(),
        name="cart-item-remove",
    ),
    path("cart/add/", CartAddView.as_view(), name="cart-add"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("", OrderListView.as_view(), name="order-list"),
    path(
        "<int:order_id>/status/",
        OrderStatusUpdateView.as_view(),
        name="order-status-update",
    ),
]
#     path(
#         "items/<int:item_id>/status/",
#         OrderItemStatusUpdateView.as_view(),
#         name="order-item-status-update",
#     ),
# ]
