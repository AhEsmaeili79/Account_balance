from modules.months import Months
from transactions.models import Transactions,Category
from django.db.models import Sum

report_data = []

# change format of date and time to shamsi
def format_date_time(transaction):
    Tr_date,Tr_time = transaction.transaction_date,transaction.transaction_time
    if Tr_date:
        transaction.transaction_date = Tr_date.strftime('%Y/%m/%d')
    if Tr_time:
        transaction.transaction_time = Tr_time.strftime('%H:%M')
    return transaction


def Month_Transform(monthNum):
    monthName = Months[str(monthNum)]
    monthNum = int(monthNum)
    return monthName,monthNum

def change_format_time(transaction):
    transaction_time = [format_date_time(txn) for txn in transaction]
    return transaction_time

def filter_by_type(req,type,month):
    data_by_type = Transactions.objects.filter(user_id=req.user.id, transaction_type=type, transaction_date__month=month ).order_by('-transaction_date', '-transaction_time')
    return data_by_type

def filter_by_date(req,date):
    data = Transactions.objects.filter(user_id=req.user.id).dates('transaction_date', date).distinct().order_by(f'-transaction_date__{date}')
    return data

def year_summary(req,years,months):
    report_data = []
    for year in years:
        transactions = Transactions.objects.filter(user_id=req.user.id, transaction_date__year=year)
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

    return report_data


