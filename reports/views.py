from django.shortcuts import render,redirect
from transactions.models import Transactions,Category
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .months import Months
from collections import defaultdict
from django.db.models import Sum, Case, When, IntegerField
# Create your views here.

# change format of date and time to shamsi
def format_date_time(transaction):
    Tr_date,Tr_time = transaction.transaction_date,transaction.transaction_time
    if Tr_date:
        transaction.transaction_date = Tr_date.strftime('%Y/%m/%d')
    if Tr_time:
        transaction.transaction_time = Tr_time.strftime('%H:%M')
    return transaction


@login_required(login_url='login')
def Report(request,monthNum):
    try:
        monthNum = int(monthNum)
        if not 1 <= monthNum <= 12:
            raise ValueError("Invalid month number")
    except ValueError:
        messages.error(request, "Invalid month number.")
        return redirect('index')
    
    transaction_income = Transactions.objects.filter(user_id=request.user.id, transaction_type='income', transaction_date__month=monthNum ).order_by('-transaction_date', '-transaction_time')
    transaction_outcome = Transactions.objects.filter(user_id=request.user.id, transaction_type='outcome', transaction_date__month=monthNum ).order_by('-transaction_date', '-transaction_time')

    # Format dates and times for display
    transaction_outcome = [format_date_time(txn) for txn in transaction_outcome]
    transaction_income = [format_date_time(txn) for txn in transaction_income]
    
    context = {
        'transaction_income': transaction_income,
        'transaction_outcome' : transaction_outcome,
    }

    return render(request, 'reports/report.html', context)


@login_required(login_url='login')
def GeneralReport(request):
    # Fetching the transaction dates for years and months
    years = Transactions.objects.filter(user_id=request.user.id).dates('transaction_date', 'year').distinct().order_by('-transaction_date__year')
    months = Transactions.objects.filter(user_id=request.user.id).dates('transaction_date', 'month').distinct().order_by('-transaction_date__month')

    # Extract year and month values
    years = [year.year for year in years]
    
    # Prepare a list of year data instead of dictionaries for easier template rendering
    report_data = []

    # Populate year_summary
    for year in years:
        transactions = Transactions.objects.filter(user_id=request.user.id, transaction_date__year=year)
        total_income = transactions.filter(transaction_type='income').aggregate(total_income=Sum('amount'))['total_income'] or 0
        total_outcome = transactions.filter(transaction_type='outcome').aggregate(total_outcome=Sum('amount'))['total_outcome'] or 0

        # Store month-wise and category-wise summaries
        months_data = []
        for month in months:
            if month.year == year:
                # Convert month number to Persian month name
                month_name = Months[str(month.month)]
                
                month_transactions = transactions.filter(transaction_date__month=month.month)
                month_income = month_transactions.filter(transaction_type='income').aggregate(total_income=Sum('amount'))['total_income'] or 0
                month_outcome = month_transactions.filter(transaction_type='outcome').aggregate(total_outcome=Sum('amount'))['total_outcome'] or 0

                # Category-wise summary
                categories_data = []
                categories = Category.objects.all()
                for category in categories:
                    category_transactions = month_transactions.filter(category_id=category)
                    category_income = category_transactions.filter(transaction_type='income').aggregate(total_income=Sum('amount'))['total_income'] or 0
                    category_outcome = category_transactions.filter(transaction_type='outcome').aggregate(total_outcome=Sum('amount'))['total_outcome'] or 0
                    if category_income > 0 or category_outcome > 0:
                        categories_data.append({
                            'category_name': category.category_name,
                            'total_income': category_income,
                            'total_outcome': category_outcome
                        })

                months_data.append({
                    'month_name': month_name,
                    'total_income': month_income,
                    'total_outcome': month_outcome,
                    'categories': categories_data
                })

        report_data.append({
            'year': year,
            'total_income': total_income,
            'total_outcome': total_outcome,
            'months': months_data
        })
        
    context = {
        'report_data': report_data,
    }
    return render(request,'reports/GeneralReport.html',context)