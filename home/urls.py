# persian_datetime/urls.py

from django.urls import path
from .views import show_balacne 

urlpatterns = [
    path('', show_balacne, name='home'),
]
