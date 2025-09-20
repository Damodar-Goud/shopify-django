from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Order, OrderItem, CartItem
from products.models import Product
from .serializers import (
    OrderSerializer,
    OrderStatusUpdateSerializer,OrderItemStatusUpdateSerializer
)
from rest_framework.permissions import IsAuthenticated


# ✅ Add to cart
class CartAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        if quantity < 1:
            return Response({"detail": "Quantity must be at least 1"}, status=400)

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
        cart.total_price = sum(item.price * item.quantity for item in cart.items.all())
        serializer = OrderSerializer(cart)
        return Response(serializer.data)


# ✅ Update cart item
class CartUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = get_object_or_404(Order, user=request.user, status="pending")
        item_id = request.data.get("item_id")
        quantity = int(request.data.get("quantity", 1))
        if quantity < 1:
            return Response({"message": "Quantity must be at least 1"}, status=400)
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
<<<<<<< HEAD
        # ✅ Recalculate total
        cart.total_price = sum(item.price * item.quantity for item in cart.items.all())

        cart.status = "paid"  # mark as placed/paid
=======
        cart.total_price = sum(item.price * item.quantity for item in cart.items.all())
        cart.status = "placed"  # mark as placed/paid
>>>>>>> 4a79d612d7d4dd1d87c45cb1bc0075b5995ea689
        cart.save()

        return Response({"message": "Order placed successfully", "order_id": cart.id})


# ✅ List Orders
class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).exclude(status="pending")
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


# orders/views.py
from rest_framework.permissions import IsAdminUser


class OrderStatusUpdateView(APIView):
    permission_classes = [IsAdminUser]  # only admin can update

    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        # ✅ check if this user is a vendor of any product in this order
        is_vendor = order.items.filter(product__vendor=request.user).exists()
        if not is_vendor:
            return Response(
                {"detail": "You do not have permission to update this order."},
                status=403,
            )

        serializer = OrderStatusUpdateSerializer(order, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Order status updated", "status": order.status})
        return Response(serializer.errors, status=400)


# orders/views.py
# class OrderItemStatusUpdateView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, item_id):
#         item = get_object_or_404(OrderItem, id=item_id)

#         # ✅ only vendor of this product can update
#         if item.product.vendor != request.user:
#             return Response({"detail": "You do not have permission to update this item."}, status=403)

#         serializer = OrderItemStatusUpdateSerializer(item, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Order item status updated", "status": item.status})
#         return Response(serializer.errors, status=400)
