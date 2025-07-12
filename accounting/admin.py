from django.contrib import admin
from .models import (
    Account, FiscalYear, FiscalPeriod, JournalEntry, JournalEntryLine, VATRate,
    Partner, Invoice, Payment, Currency, ExchangeRate, Journal
)

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'type', 'vat_applicable')
    search_fields = ('code', 'name')
    list_filter = ('type', 'vat_applicable')

@admin.register(FiscalYear)
class FiscalYearAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'end_date', 'is_closed')
    ordering = ('-start_date',)

@admin.register(FiscalPeriod)
class FiscalPeriodAdmin(admin.ModelAdmin):
    list_display = ('fiscal_year', 'start_date', 'end_date', 'is_closed')
    ordering = ('fiscal_year', 'start_date')

class JournalEntryLineInline(admin.TabularInline):
    model = JournalEntryLine
    extra = 1

@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'journal', 'fiscal_year', 'fiscal_period', 'description', 'created_at', 'created_by')
    list_filter = ('date', 'fiscal_year', 'fiscal_period', 'journal')
    inlines = [JournalEntryLineInline]

@admin.register(VATRate)
class VATRateAdmin(admin.ModelAdmin):
    list_display = ('name', 'rate')

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'vat_number', 'is_customer', 'is_supplier')
    search_fields = ('name', 'vat_number')

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('number', 'partner', 'invoice_date', 'due_date', 'total_amount', 'currency', 'is_paid')
    list_filter = ('invoice_date', 'due_date', 'is_paid')
    search_fields = ('number', 'partner__name')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'payment_date', 'amount', 'currency', 'payment_method')
    list_filter = ('payment_date', 'payment_method')

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'symbol')

@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('currency', 'date', 'rate')
    ordering = ('-date',)

@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
