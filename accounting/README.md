# Accounting Django App

Welcome to the Accounting Django App! This reusable app is designed to help you manage the complete accounting and financial books of a Belgian company, fully compliant with Belgian accounting rules and laws.

## Key Features

- Comprehensive Belgian chart of accounts support
- Manage customers and suppliers with the Partner model
- Create and track invoices and payments
- Multi-currency support with exchange rates
- Detailed VAT handling as per Belgian tax regulations
- Fiscal year and fiscal period management with closing capabilities
- Journals and balanced journal entries with audit trails
- Fully integrated Django admin interface for easy management

## Installation

1. Copy the `accounting` app folder into your Django project directory.
2. Add `'accounting'` to the `INSTALLED_APPS` list in your Django project's `settings.py` file.
3. Run the migrations to create the necessary database tables:
   ```bash
   python manage.py makemigrations accounting
   python manage.py migrate
   ```
4. Include the app's URLs in your project's `urls.py`:
   ```python
   from django.urls import include, path

   urlpatterns = [
       # ... your other url patterns
       path('accounting/', include('accounting.urls')),
   ]
   ```

## Usage

- Use the Django admin site to manage accounts, partners, invoices, payments, VAT rates, fiscal years, and journal entries.
- The app provides basic views for listing and viewing accounts and journal entries.
- Extend or customize the app as needed to fit your specific business requirements.

## Notes

- This app is tailored to Belgian accounting standards but can be adapted for other jurisdictions.
- Ensure you have proper backups and testing before using in a production environment.
- Contributions and improvements are welcome!

## Support

For any questions or issues, please open an issue or contact the maintainer.

Enjoy managing your accounting with ease and compliance!

---

*Crafted with care by Milton Chadwick*
