from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from modules.utils_repo import change_format_time
from modules.utils_trans import has_transaction,check_int ,filter_by_type,get_from_post,update_trans,create_trans,is_valid_datetime
from .models import Category, Transactions
from datetime import datetime, timedelta


@login_required(login_url='login')
def show_category(request):
    context = {}
    if request.user.is_authenticated:
        if request.method == 'POST':
            category_name = request.POST.get('cat_name')
            user_id = request.POST.get('user_id')
            
            if not category_name:
                messages.error(request, 'Category name cannot be empty.')
            elif Category.objects.filter(category_name=category_name, user_id=user_id).exists():
                messages.error(request, 'You have already created this category.')
            else:
                category = Category(category_name=category_name, user_id=user_id)
                category.save()
                return redirect('add_category')
        
        category_list = Category.objects.filter(user_id=0)
        category_user_add = Category.objects.filter(user_id=request.user.id)
        context = {
            'category': category_list,
            'category_user': category_user_add
        }
    
    return render(request, 'transactions/category.html', context)



@login_required(login_url='login')
def transaction(request):
    if 'add_transaction' in request.POST:
        amount,transaction_date,transaction_time,transaction_category,user_id,description = get_from_post(request,'amount',
                                                                                                          'transactionDate',
                                                                                                          'transactionTime',
                                                                                                          'category',
                                                                                                          'user_id',
                                                                                                          'description')
        transaction_type = request.POST.get('transactionType')
        
        if check_int(amount):
            if amount and transaction_type and transaction_date and transaction_time and transaction_category:
                transaction_date = transaction_date.replace('/', '-')
                if is_valid_datetime(transaction_date, transaction_time):
                    transaction_exists = has_transaction(amount, transaction_type, transaction_date,transaction_category, user_id, transaction_time, description)
                    if not transaction_exists:
                        transaction = create_trans(amount,transaction_type,transaction_date,
                                                transaction_time,transaction_category,
                                                user_id,description)
                        transaction.save()
                        return redirect('add_transactions')
                    else:
                        messages.error(request,"این تراکنش در سیستم وجود دارد!")
                        return redirect('add_transactions')
                else:
                        messages.error(request,"تاریخ و زمان را به صورت درست وارد کنید")
            else:
                    messages.error(request, "تمام مقادیر را وارد کنید")
        else:
            messages.error(request,"لطفا مقدار را عدد وارد کنید")

    
    transaction_income = filter_by_type(request,'income')
    transaction_outcome = filter_by_type(request,'outcome')
    
    category_list = Category.objects.filter(user_id=0) | Category.objects.filter(user_id=request.user.id)

    # Format dates and times for display
    tr_income = change_format_time(transaction_income)
    tr_outcome = change_format_time(transaction_outcome)

    context = {
        'transaction_outcome': tr_outcome,
        'transaction_income': tr_income,
        'category': category_list,
    }

    return render(request, 'transactions/transactions.html', context)


@login_required(login_url='login')
def edit_transaction(request):
    if 'edit_transaction' in request.POST:
        transaction_id = request.POST.get('transaction_id')

        amount_update,transaction_date_update,transaction_time_update,transaction_category_update,user_id,description_update = get_from_post(request,'amount',
                                                                                                                                             'transactionDate',
                                                                                                                                             'transactionTime',
                                                                                                                                             'category',
                                                                                                                                             'user_id',
                                                                                                                                             'description')

        transaction = get_object_or_404(Transactions,id=transaction_id)
        
        transaction_date_update = transaction_date_update.replace('/', '-')
        if is_valid_datetime(transaction_date_update, transaction_time_update):
            trsnation = update_trans(transaction, amount_update, transaction_date_update,
                                    transaction_time_update,transaction_category_update,
                                    user_id,description_update)

            trsnation.save()
            return redirect('add_transactions')
        else:
            messages.error(request," تاریخ و زمان را به صورت درست وارد کنید و حتما دارای ثانیه باشد.")
            return redirect('add_transactions')
    
    return render(request, 'transactions/transactions.html')


@login_required(login_url='login')
def delete_transaction(request):
    if 'delete_transaction' in request.POST:
        transaction_id = request.POST.get('transaction_id')
        transaction_delete = Transactions.objects.filter(id=transaction_id)
        transaction_delete.delete()

        messages.success(request,"تراکنش با موفقیت حذف شد.")
        return redirect('add_transactions')
    else:
        messages.error(request,"حذف تراکنش با شکست مواجه شد.")
        return redirect('add_transactions')