from django.utils import timezone
from persiantools.jdatetime import JalaliDate
import pytz

def get_persian_datetime():
    # Define the timezone for Iran
    iran_tz = pytz.timezone('Asia/Tehran')
    
    # Get the current time in UTC and convert it to Iran's timezone
    now = timezone.now().astimezone(iran_tz)
    
    # Convert to Jalali date
    persian_date = JalaliDate(now).strftime('%Y-%m-%d')
    
    # Format time in Iran's timezone
    persian_time = now.strftime('%H:%M:%S')
    
    return persian_date, persian_time
