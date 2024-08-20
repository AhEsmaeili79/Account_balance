# persian_datetime/urls.py

from django.urls import path
from .views import Report,GeneralReport

urlpatterns = [
    path('month=<int:monthNum>', Report, name='report'),
    path('generalreport', GeneralReport, name='generalreport')
]
