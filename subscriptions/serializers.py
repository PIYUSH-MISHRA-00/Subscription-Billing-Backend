from rest_framework import serializers
from .models import Plan, Subscription, Invoice

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'name', 'price', 'description']

class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'plan', 'start_date', 'end_date', 'status']

class InvoiceSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)
    class Meta:
        model = Invoice
        fields = ['id', 'user', 'plan', 'subscription', 'amount', 'issue_date', 'due_date', 'status']
