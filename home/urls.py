# persian_datetime/urls.py

from django.urls import path
from .views import show_balacne ,get_transactions_data

urlpatterns = [
    path('', show_balacne, name='index'),
    path('api/transactions/', get_transactions_data, name='get_transactions_data'),
]
