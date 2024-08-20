from django.shortcuts import render,redirect
from transactions.models import Transactions
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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