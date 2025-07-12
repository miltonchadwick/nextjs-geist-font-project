# Django Accounting App

This repository contains a reusable Django app for managing accounting and financial books, specifically designed for Belgian companies and compliant with Belgian accounting rules and laws.

## What's Included

The `accounting/` directory contains a complete Django app with:

- **Models**: Comprehensive accounting models including accounts, partners, invoices, payments, VAT rates, fiscal years, and journal entries
- **Admin Interface**: Fully configured Django admin for managing all accounting data
- **Views**: Basic CRUD views for accounts and journal entries
- **Forms**: Django forms for data input and validation
- **Belgian Compliance**: Designed specifically for Belgian accounting standards and tax regulations

## Quick Start

1. Copy the `accounting/` folder into your Django project
2. Add `'accounting'` to your `INSTALLED_APPS` in settings.py
3. Run migrations:
   ```bash
   python manage.py makemigrations accounting
   python manage.py migrate
   ```
4. Include URLs in your project's urls.py:
   ```python
   path('accounting/', include('accounting.urls')),
   ```

## Features

- Multi-currency support with exchange rates
- Partner management (customers/suppliers)
- Invoice and payment tracking
- VAT handling for Belgian tax compliance
- Fiscal year and period management
- Balanced journal entries with audit trails
- Comprehensive Django admin interface

For detailed documentation, see `accounting/README.md`.

---

*Crafted with care by Milton Chadwick*
