from django.shortcuts import render
from .utils import get_persian_datetime

def persian_datetime_view(request):
    persian_date, persian_time = get_persian_datetime()
    context = {
        'persian_date': persian_date,
        'persian_time': persian_time,
    }
    return render(request, 'persian_datetime/datetime.html', context)
