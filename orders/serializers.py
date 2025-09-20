from rest_framework import serializers
from .models import CartItem, Order, OrderItem
from products.serializers import ProductSerializer
from products.models import Product

from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer  # ✅ make sure this exists


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()  # dynamically calculate total

    class Meta:
        model = Order
        fields = ["id", "status", "total_price", "created_at", "items"]

    def get_total_price(self, obj):
        return sum(item.price * item.quantity for item in obj.items.all())


<<<<<<< HEAD
# orders/serializers.py
=======
# Optional: Serializer to update order status (admin or automated updates)
>>>>>>> 4a79d612d7d4dd1d87c45cb1bc0075b5995ea689
class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status"]
<<<<<<< HEAD


# orders/serializers.py
class OrderItemStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["status"]
=======
>>>>>>> 4a79d612d7d4dd1d87c45cb1bc0075b5995ea689
