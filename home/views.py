from django.shortcuts import render
from transactions.models import Balance
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from transactions.models import Transactions
from django.http import JsonResponse
from django.db.models import Sum
import json

@login_required(login_url='login')
def show_balacne(request):
    if User.is_authenticated:
        balance = Balance.objects.all().filter(user_id=request.user.id)
    else:
        balance = "please login"

    context ={
        'balance' : balance
    }

    return render(request,'home/index.html',context)


def get_transactions_data(request):
    # Assuming you want data grouped by month
    transactions = Transactions.objects.values('transaction_date__month', 'transaction_type').annotate(total_amount=Sum('amount'))

    # Prepare data for JSON response
    data = {
        'income': [0] * 12,
        'outcome': [0] * 12
    }

    for transaction in transactions:
        month = transaction['transaction_date__month'] - 1  # Convert to zero-based index
        if transaction['transaction_type'] == 'income':
            data['income'][month] = transaction['total_amount']
        else:
            data['outcome'][month] = transaction['total_amount']

    return JsonResponse(data)