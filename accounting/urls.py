from django.urls import path
from . import views

app_name = 'accounting'

urlpatterns = [
    path('accounts/', views.AccountListView.as_view(), name='account-list'),
    path('accounts/<int:pk>/', views.AccountDetailView.as_view(), name='account-detail'),
    path('journal-entries/', views.JournalEntryListView.as_view(), name='journalentry-list'),
    path('journal-entries/<int:pk>/', views.JournalEntryDetailView.as_view(), name='journalentry-detail'),
]
