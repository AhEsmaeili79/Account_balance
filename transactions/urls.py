# persian_datetime/urls.py

from django.urls import path
from .views import show_category,transaction,edit_transaction

urlpatterns = [
    path('category', show_category, name='add_category'),
    path('', transaction, name='add_transactions'),
    path('',edit_transaction,name='edit_transactions'),
]
