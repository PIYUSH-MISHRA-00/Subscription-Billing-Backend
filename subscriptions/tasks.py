from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Subscription, Invoice

@shared_task
def generate_invoices():
    today = timezone.now().date()
    subs = Subscription.objects.filter(start_date=today, status='active')
    for sub in subs:
        Invoice.objects.create(
            user=sub.user,
            plan=sub.plan,
            subscription=sub,
            amount=sub.plan.price,
            issue_date=today,
            due_date=today + timedelta(days=7),
            status='pending',
        )
        print(f"Invoice generated for {sub.user.username} - {sub.plan.name}")

@shared_task
def mark_overdue_invoices():
    today = timezone.now().date()
    overdue = Invoice.objects.filter(status='pending', due_date__lt=today)
    for invoice in overdue:
        invoice.status = 'overdue'
        invoice.save()
        print(f"Invoice {invoice.id} marked as overdue.")

@shared_task
def send_unpaid_reminders():
    unpaid = Invoice.objects.filter(status='pending')
    for invoice in unpaid:
        print(f"Reminder: Invoice {invoice.id} for {invoice.user.email} is still unpaid.")
