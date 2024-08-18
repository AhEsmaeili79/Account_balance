# persian_datetime/urls.py

from django.urls import path
from .views import show_category 

urlpatterns = [
    path('', show_category, name='add_category'),
]
