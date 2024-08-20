from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import JsonResponse
from transactions.models import Transactions

@login_required(login_url='login')
def show_balacne(request):
    if User.is_authenticated:
            # Total amount for 'income' type
        income_total = Transactions.objects.filter(
            user_id=request.user.id, 
            transaction_type='income'
        ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

        # Total amount for 'outcome' type
        outcome_total = Transactions.objects.filter(
            user_id=request.user.id, 
            transaction_type='outcome'
        ).aggregate(total_amount=Sum('amount'))['total_amount'] or 0

        
        balance = income_total - outcome_total


    # Generate a list of years based on the transactions data
    years = Transactions.objects.filter(user_id=request.user.id).dates('transaction_date', 'year').distinct().order_by('-transaction_date__year')
    years = [year.year for year in years]  # Extract just the year values

    context = {
        'balance': balance,
        'years': years
    }

    return render(request,'home/index.html',context)


@login_required(login_url='login')
def get_transactions_data(request):
    year = request.GET.get('year', None)
    
    if not year:
        return JsonResponse({'error': 'Year parameter is required'}, status=400)

    try:
        year = int(year)
    except ValueError:
        return JsonResponse({'error': 'Invalid year parameter'}, status=400)

    transactions = Transactions.objects.filter(user_id=request.user.id,transaction_date__year=year) \
        .values('transaction_date__month', 'transaction_type') \
        .annotate(total_amount=Sum('amount'))

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