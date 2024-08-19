# persian_datetime/urls.py

from django.urls import path
from .views import show_category,transaction

urlpatterns = [
    path('category', show_category, name='add_category'),
    path('', transaction, name='transactions'),
]
