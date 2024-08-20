# persian_datetime/urls.py

from django.urls import path
from .views import Report

urlpatterns = [
    path('month=<int:monthNum>', Report, name='report'),
    
]
