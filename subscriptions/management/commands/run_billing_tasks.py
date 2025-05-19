from django.core.management.base import BaseCommand
from subscriptions.tasks import generate_invoices, mark_overdue_invoices, send_unpaid_reminders

class Command(BaseCommand):
    help = 'Run all periodic billing tasks (for development/testing)'

    def handle(self, *args, **kwargs):
        generate_invoices()
        mark_overdue_invoices()
        send_unpaid_reminders()
        self.stdout.write(self.style.SUCCESS('All billing tasks executed.'))
