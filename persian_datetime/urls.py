# persian_datetime/urls.py

from django.urls import path
from .views import persian_datetime_view

urlpatterns = [
    path('', persian_datetime_view, name='persian_datetime'),
]
