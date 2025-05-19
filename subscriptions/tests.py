from django.test import TestCase
from django.contrib.auth.models import User
from .models import Plan, Subscription, Invoice
from django.urls import reverse
from rest_framework.test import APIClient
from datetime import date, timedelta

class PlanModelTest(TestCase):
    def test_create_plan(self):
        plan = Plan.objects.create(name='basic', price=10.00, description='Basic Plan')
        self.assertEqual(str(plan), 'Basic')

class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.plan = Plan.objects.create(name='pro', price=20.00, description='Pro Plan')

    def test_create_subscription(self):
        sub = Subscription.objects.create(user=self.user, plan=self.plan, start_date=date.today(), end_date=date.today()+timedelta(days=30), status='active')
        self.assertEqual(str(sub), f"{self.user.username} - {self.plan.name} (active)")

class InvoiceModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser2', password='testpass')
        self.plan = Plan.objects.create(name='enterprise', price=50.00, description='Enterprise Plan')
        self.sub = Subscription.objects.create(user=self.user, plan=self.plan, start_date=date.today(), end_date=date.today()+timedelta(days=30), status='active')

    def test_create_invoice(self):
        invoice = Invoice.objects.create(user=self.user, plan=self.plan, subscription=self.sub, amount=50.00, issue_date=date.today(), due_date=date.today()+timedelta(days=7), status='pending')
        self.assertEqual(str(invoice), f"Invoice #{invoice.id} - {self.user.username} - pending")

class SubscriptionAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='apitest', password='testpass')
        self.plan = Plan.objects.create(name='basic', price=10.00, description='Basic Plan')
        self.client.force_authenticate(user=self.user)

    def test_subscribe(self):
        response = self.client.post(reverse('subscribe'), {'plan_id': self.plan.id})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['plan']['name'], 'basic')

    def test_unsubscribe(self):
        self.client.post(reverse('subscribe'), {'plan_id': self.plan.id})
        response = self.client.post(reverse('unsubscribe'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.data)

    def test_invoice_list(self):
        # Subscribe to create a subscription
        self.client.post(reverse('subscribe'), {'plan_id': self.plan.id})
        # No invoices yet, but endpoint should work
        response = self.client.get(reverse('invoice-list'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
