from django.views.generic import ListView, DetailView
from .models import Account, JournalEntry

class AccountListView(ListView):
    model = Account
    template_name = 'accounting/account_list.html'
    context_object_name = 'accounts'

class AccountDetailView(DetailView):
    model = Account
    template_name = 'accounting/account_detail.html'
    context_object_name = 'account'

class JournalEntryListView(ListView):
    model = JournalEntry
    template_name = 'accounting/journalentry_list.html'
    context_object_name = 'journal_entries'

class JournalEntryDetailView(DetailView):
    model = JournalEntry
    template_name = 'accounting/journalentry_detail.html'
    context_object_name = 'journal_entry'
