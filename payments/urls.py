from django.urls import path
from .views import CreateOrderView, PaymentWebhookView

urlpatterns = [
    path("create-order/", CreateOrderView.as_view(), name="create-order"),
    path("webhook/", PaymentWebhookView.as_view(), name="razorpay-webhook"),
]
