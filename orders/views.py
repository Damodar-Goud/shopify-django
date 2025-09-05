from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Order, OrderItem, CartItem
from products.models import Product
from .serializers import (
    OrderSerializer,
)
from rest_framework.permissions import IsAuthenticated


# ✅ Add to cart
class CartAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        if not product_id:
            return Response({"detail": "Product ID is required"}, status=400)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found"}, status=404)

        # ✅ Get or create cart
        order, _ = Order.objects.get_or_create(user=request.user, status="pending")

        # ✅ Get or create order item
        item, created = OrderItem.objects.get_or_create(
            order=order,
            product=product,
            defaults={"quantity": quantity, "price": product.price},
        )

        if not created:
            item.quantity += quantity
            item.save()

        return Response({"detail": "Added to cart"}, status=200)


# ✅ View Cart
class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Order.objects.get_or_create(user=request.user, status="pending")
        serializer = OrderSerializer(cart)
        return Response(serializer.data)


# ✅ Update cart item
class CartUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = get_object_or_404(Order, user=request.user, status="pending")
        item_id = request.data.get("item_id")
        quantity = request.data.get("quantity")

        item = get_object_or_404(cart.items, id=item_id)
        item.quantity = quantity
        item.save()
        return Response({"message": "Quantity updated"})


# ✅ Remove cart item
class CartRemoveView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = get_object_or_404(Order, user=request.user, status="pending")
        item_id = request.data.get("item_id")
        item = get_object_or_404(cart.items, id=item_id)
        item.delete()
        return Response({"message": "Item removed"})


# ✅ Checkout
class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = get_object_or_404(Order, user=request.user, status="pending")
        cart.status = "paid"  # mark as placed/paid
        cart.save()
        return Response({"message": "Order placed successfully"})


# ✅ List Orders
class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).exclude(status="pending")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
