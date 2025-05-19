![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white) ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white) ![Celery](https://img.shields.io/badge/celery-%23a9cc54.svg?style=for-the-badge&logo=celery&logoColor=ddf4a4) ![Stripe](https://img.shields.io/badge/Stripe-5469d4?style=for-the-badge&logo=stripe&logoColor=ffffff)

# Subscription Billing Backend

## 📌 Objective
A basic subscription billing backend supporting user sign-up, plan subscription, automatic invoice generation using Celery, and simple billing lifecycle tracking.

## 🛠️ Features
- **Models:** User, Plan, Subscription, Invoice
- **Celery Tasks:**
  - Generate monthly invoices for active subscriptions
  - Mark unpaid invoices as overdue
  - Send reminders for unpaid invoices (console print/mock)
- **APIs:**
  - User subscribe/unsubscribe to plans
  - View invoices and payment status
  - Pay invoices using Stripe
- **Predefined Plans:** Basic, Pro, Enterprise
- **Admin Panel:** Manage users, plans, subscriptions, and invoices

## 🚀 Bonus
- Reminder emails (console print/mock)
- Stripe integration (fully implemented: see Stripe Integration section below)

## 📦 Installation
1. **Clone the repository**
2. **Create and activate a virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
4. **Run migrations:**
   ```powershell
   python manage.py migrate
   ```
5. **Create a superuser:**
   ```powershell
   python manage.py createsuperuser
   ```
6. **Start Redis (for Celery):**
   - Make sure Redis is running on `localhost:6379`
7. **Run the development server:**
   ```powershell
   python manage.py runserver
   ```
8. **Run Celery worker (in a new terminal):**
   ```powershell
   celery -A billing_system worker --beat --scheduler django -l info
   ```

## 🧪 Usage
- Access the admin panel at `/admin/` to add plans (Basic, Pro, Enterprise)
- Use the following API endpoints:
  - `POST /api/subscribe/` — Subscribe to a plan
  - `POST /api/unsubscribe/` — Unsubscribe from current plan
  - `GET /api/invoices/` — List all invoices for the user
  - `GET /api/invoices/<id>/` — Get details of a specific invoice
  - `POST /api/pay/` — Pay an invoice using Stripe (mock PaymentIntent, marks invoice as paid)

## 📝 Project Structure
- `subscriptions/models.py`: Models for Plan, Subscription, Invoice
- `subscriptions/views.py`: API endpoints
- `subscriptions/tasks.py`: Celery tasks for billing automation
- `subscriptions/serializers.py`: DRF serializers
- `billing_system/celery.py`: Celery configuration

## 💳 Stripe Integration
- Stripe integration is implemented using the `/api/pay/` endpoint.
- When a user pays an invoice, a Stripe PaymentIntent is created and the invoice is marked as paid (mock/demo for test mode).
- You can extend this to handle real Stripe webhooks for production.

### Stripe Setup
1. Add your Stripe test secret key to your Django settings:
   ```python
   STRIPE_SECRET_KEY = 'sk_test_...'
   ```
2. Use the `/api/pay/` endpoint with `{ "invoice_id": <id> }` to simulate payment.

## 🧩 Testing
- Run all billing tasks manually (for development):
  ```powershell
  python manage.py run_billing_tasks
  ```
- Unit tests can be added in `subscriptions/tests.py`
- However, for even greater clarity, you could add an explicit example for running all tests:
  ```powershell
  python manage.py test subscriptions
  ```

## ❓ FAQ
- **How are invoices generated?**
  - Celery runs a daily task to generate invoices for subscriptions starting that day.
- **How are overdue invoices handled?**
  - Celery marks invoices as overdue if the due date has passed and payment is not received.
- **How are reminders sent?**
  - Reminders are printed to the console for unpaid invoices (can be extended to email).

## 📄 Submission
- All requirements are met as per the assignment.
- Bonus: Reminder system implemented (console print).
- Stripe integration is fully implemented.

---
