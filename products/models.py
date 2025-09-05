from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Product(models.Model):
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(
        upload_to="products/", blank=True, null=True
    )  # local for now, later AWS S3
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
