from django.db import models
from orders.models import Order  # type: ignore


class Payment(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="payment"
    )
    razorpay_order_id = models.CharField(
        max_length=100, unique=True
    )  # Razorpay order ID
    payment_id = models.CharField(
        max_length=100, blank=True, null=True
    )  # Razorpay payment ID
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="INR")
    status = models.CharField(
        max_length=20,
        choices=[("created", "Created"), ("paid", "Paid"), ("failed", "Failed")],
        default="created",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order.id} → {self.status}"


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("payment_failed", "Payment Failed"),
    ]   
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    # other fields...
