# persian_datetime/urls.py

from django.urls import path
from .views import show_category,transaction,edit_transaction,delete_transaction,delete_category,edit_category

urlpatterns = [
    path('category', show_category, name='add_category'),
    path('', transaction, name='add_transactions'),
    path('edit',edit_transaction,name='edit_transactions'),
    path('delete',delete_transaction,name='delete_transactions'),
    path('delete-cat',delete_category,name='delete_category'),
    path('edit-cat',edit_category,name='edit_category'),
]
