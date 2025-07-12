from django import forms
from .models import JournalEntry, JournalEntryLine

class JournalEntryLineForm(forms.ModelForm):
    class Meta:
        model = JournalEntryLine
        fields = ['account', 'debit', 'credit', 'description']

class JournalEntryForm(forms.ModelForm):
    lines = forms.inlineformset_factory(
        JournalEntry,
        JournalEntryLine,
        form=JournalEntryLineForm,
        extra=1,
        can_delete=True
    )

    class Meta:
        model = JournalEntry
        fields = ['date', 'description', 'fiscal_year']
