from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class Currency(models.Model):
    """
    Currency model for multi-currency support.
    """
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.code} - {self.name}"

class ExchangeRate(models.Model):
    """
    Exchange rate for currencies.
    """
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    date = models.DateField()
    rate = models.DecimalField(max_digits=12, decimal_places=6)

    class Meta:
        unique_together = ('currency', 'date')

    def __str__(self):
        return f"{self.currency.code} rate on {self.date}: {self.rate}"

class Account(models.Model):
    """
    Account model based on Belgian chart of accounts.
    """
    class AccountType(models.TextChoices):
        ASSET = 'AS', _('Asset')
        LIABILITY = 'LI', _('Liability')
        EQUITY = 'EQ', _('Equity')
        REVENUE = 'RE', _('Revenue')
        EXPENSE = 'EX', _('Expense')

    code = models.CharField(max_length=10, unique=True, help_text="Account code as per Belgian chart of accounts")
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=2, choices=AccountType.choices)
    vat_applicable = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.code} - {self.name}"

class Partner(models.Model):
    """
    Partner model for customers and suppliers.
    """
    name = models.CharField(max_length=255)
    vat_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_customer = models.BooleanField(default=False)
    is_supplier = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class FiscalYear(models.Model):
    """
    Fiscal year for accounting period management.
    """
    start_date = models.DateField()
    end_date = models.DateField()
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return f"Fiscal Year {self.start_date.year}"

class FiscalPeriod(models.Model):
    """
    Fiscal period within a fiscal year.
    """
    fiscal_year = models.ForeignKey(FiscalYear, on_delete=models.CASCADE, related_name='periods')
    start_date = models.DateField()
    end_date = models.DateField()
    is_closed = models.BooleanField(default=False)

    def __str__(self):
        return f"Period {self.start_date} to {self.end_date}"

class Journal(models.Model):
    """
    Journal for grouping journal entries.
    """
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class JournalEntry(models.Model):
    """
    Journal entry with debit and credit lines.
    """
    journal = models.ForeignKey(Journal, on_delete=models.PROTECT)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    fiscal_year = models.ForeignKey(FiscalYear, on_delete=models.PROTECT)
    fiscal_period = models.ForeignKey(FiscalPeriod, on_delete=models.PROTECT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_journal_entries')
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_journal_entries')

    def __str__(self):
        return f"Journal Entry {self.id} on {self.date}"

    def clean(self):
        from django.core.exceptions import ValidationError
        total_debit = sum(line.debit for line in self.lines.all())
        total_credit = sum(line.credit for line in self.lines.all())
        if total_debit != total_credit:
            raise ValidationError("Journal entry is not balanced: total debit does not equal total credit.")

class JournalEntryLine(models.Model):
    """
    Lines for journal entries representing debit or credit.
    """
    journal_entry = models.ForeignKey(JournalEntry, related_name='lines', on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    debit = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    credit = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    description = models.CharField(max_length=255, blank=True, null=True)
    vat_rate = models.ForeignKey('VATRate', on_delete=models.SET_NULL, null=True, blank=True)
    partner = models.ForeignKey(Partner, on_delete=models.SET_NULL, null=True, blank=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.debit > 0 and self.credit > 0:
            raise ValidationError("A line cannot have both debit and credit amounts.")
        if self.debit == 0 and self.credit == 0:
            raise ValidationError("A line must have either debit or credit amount.")

    def __str__(self):
        return f"{self.account} - Debit: {self.debit} Credit: {self.credit}"

class VATRate(models.Model):
    """
    VAT rates applicable in Belgium.
    """
    name = models.CharField(max_length=50)
    rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="VAT rate percentage")

    def __str__(self):
        return f"{self.name} ({self.rate}%)"

class Invoice(models.Model):
    """
    Invoice model for sales and purchases.
    """
    partner = models.ForeignKey(Partner, on_delete=models.PROTECT)
    invoice_date = models.DateField()
    due_date = models.DateField()
    number = models.CharField(max_length=50, unique=True)
    fiscal_year = models.ForeignKey(FiscalYear, on_delete=models.PROTECT)
    fiscal_period = models.ForeignKey(FiscalPeriod, on_delete=models.PROTECT, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice {self.number} - {self.partner.name}"

class Payment(models.Model):
    """
    Payment model linked to invoices.
    """
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    payment_method = models.CharField(max_length=50)

    def __str__(self):
        return f"Payment of {self.amount} on {self.payment_date} for Invoice {self.invoice.number}"
