from django.shortcuts import render
import razorpay
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

import razorpay
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from orders.models import Order

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


class CreateOrderView(APIView):
    def post(self, request):
        razorpay_order_id = request.data.get("razorpay_order_id")  # our DB order id
        amount = request.data.get("amount")

        try:
            order = Order.objects.get(id=razorpay_order_id)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if not amount:
            return Response(
                {"error": "Amount required"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Razorpay expects amount in paise
        order_data = {
            "amount": int(float(amount) * 100),
            "currency": "INR",
            "payment_capture": "1",
        }
        razorpay_order = client.order.create(order_data)

        payment = Payment.objects.create(
            order=order,
            razorpay_order_id=razorpay_order["id"],
            amount=amount,
            currency="INR",
            status="created",
        )

        return Response(
            {
                "razorpay_order_id": razorpay_order["id"],
                "amount": amount,
                "currency": "INR",
                "key": settings.RAZORPAY_KEY_ID,
            }
        )


import hmac
import hashlib


class PaymentWebhookView(APIView):
    def post(self, request):
        payload = request.body
        signature = request.headers.get("X-Razorpay-Signature")
        webhook_secret = "your_webhook_secret"  # set in Razorpay dashboard

        expected_signature = hmac.new(
            webhook_secret.encode(), payload, hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(expected_signature, signature):
            return Response({"error": "Invalid signature"}, status=400)

        event = request.data
        razorpay_order_id = event["payload"]["payment"]["entity"]["razorpay_order_id"]
        payment_id = event["payload"]["payment"]["entity"]["id"]
        status_event = event["event"]

        payment = Payment.objects.filter(razorpay_order_id=razorpay_order_id).first()
        if payment:
            payment.payment_id = payment_id

            if status_event == "payment.captured":
                payment.status = "paid"
                payment.order.status = "paid"  # update order status
                payment.order.save()
            elif status_event == "payment.failed":
                payment.status = "failed"
                payment.order.status = "payment_failed"
                payment.order.save()

            payment.save()

        return Response({"status": "ok"})
