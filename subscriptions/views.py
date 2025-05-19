from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.utils import timezone
from .models import Plan, Subscription, Invoice
from .serializers import SubscriptionSerializer, InvoiceSerializer
from django.contrib.auth.models import User
from datetime import timedelta
import stripe
from django.conf import settings

# Create your views here.

class SubscribeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        plan_id = request.data.get('plan_id')
        try:
            plan = Plan.objects.get(id=plan_id)
        except Plan.DoesNotExist:
            return Response({'error': 'Plan not found.'}, status=status.HTTP_404_NOT_FOUND)
        # Cancel any existing active subscription
        Subscription.objects.filter(user=request.user, status='active').update(status='cancelled')
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=30)
        subscription = Subscription.objects.create(
            user=request.user,
            plan=plan,
            start_date=start_date,
            end_date=end_date,
            status='active',
        )
        return Response(SubscriptionSerializer(subscription).data, status=status.HTTP_201_CREATED)

class UnsubscribeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        sub = Subscription.objects.filter(user=request.user, status='active').first()
        if not sub:
            return Response({'error': 'No active subscription.'}, status=status.HTTP_400_BAD_REQUEST)
        sub.status = 'cancelled'
        sub.end_date = timezone.now().date()
        sub.save()
        return Response({'message': 'Unsubscribed successfully.'})

class InvoiceListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        invoices = Invoice.objects.filter(user=request.user)
        return Response(InvoiceSerializer(invoices, many=True).data)

class InvoiceDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            invoice = Invoice.objects.get(pk=pk, user=request.user)
        except Invoice.DoesNotExist:
            return Response({'error': 'Invoice not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(InvoiceSerializer(invoice).data)

stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', 'sk_test_...')  # Replace with your test key

class StripePaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        invoice_id = request.data.get('invoice_id')
        try:
            invoice = Invoice.objects.get(id=invoice_id, user=request.user)
        except Invoice.DoesNotExist:
            return Response({'error': 'Invoice not found.'}, status=status.HTTP_404_NOT_FOUND)
        if invoice.status == 'paid':
            return Response({'message': 'Invoice already paid.'}, status=status.HTTP_400_BAD_REQUEST)
        # Create a Stripe PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=int(invoice.amount * 100),  # Stripe expects amount in cents
            currency='usd',
            metadata={'invoice_id': invoice.id, 'user_id': request.user.id},
            description=f'Payment for Invoice #{invoice.id}',
            receipt_email=request.user.email,
        )
        invoice.status = 'paid'  # For mock/demo, mark as paid immediately
        invoice.save()
        return Response({'client_secret': intent['client_secret'], 'invoice_id': invoice.id, 'status': invoice.status})
