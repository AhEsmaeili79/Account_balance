from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from modules.utils_repo import Month_Transform,change_format_time,year_summary,filter_by_date,filter_by_type


# Create your views here.
@login_required(login_url='login')
def Report(request,monthNum):
    try:
        monthName,monthNum = Month_Transform(monthNum)
        
        if not 1 <= monthNum <= 12:
            raise ValueError("Invalid month number")
    except ValueError:
        messages.error(request, "Invalid month number.")
        return redirect('index')
    
    trans_income = filter_by_type(request,'income',monthNum)
    trans_outcome = filter_by_type(request,'outcome',monthNum)
    
    # Format dates and times for display
    trans_income = change_format_time(trans_income)
    trans_outcome = change_format_time(trans_outcome)
    
    context = {
        'transaction_income': trans_income,
        'transaction_outcome' : trans_outcome,
        'monthname': monthName,
    }

    return render(request, 'reports/report.html', context)


@login_required(login_url='login')
def GeneralReport(request):
    
    years = filter_by_date(request,'year')
    months = filter_by_date(request,'month')

    # Extract year and month values
    years = [year.year for year in years]
    
    # Prepare a list of year data instead of dictionaries for easier template rendering
    report_data = year_summary(request,years,months)
        
    context = {
        'report_data': report_data,
    }
    return render(request,'reports/GeneralReport.html',context)