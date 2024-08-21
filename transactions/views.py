from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Category, Transactions
from django.contrib.auth.decorators import login_required


# change format of date and time to shamsi
def format_date_time(transaction):
    Tr_date,Tr_time = transaction.transaction_date,transaction.transaction_time
    if Tr_date:
        transaction.transaction_date = Tr_date.strftime('%Y/%m/%d')
    if Tr_time:
        transaction.transaction_time = Tr_time.strftime('%H:%M')
    return transaction


def has_transaction(am,Tr_T,Tr_d,Tr_Cat,U_id,Tr_Time,Desc):
    has_transacion = Transactions.objects.filter(amount=am,
                                                     transaction_type=Tr_T,
                                                     transaction_date=Tr_d,
                                                     user_id=U_id,
                                                     category_id=Tr_Cat,
                                                     transaction_time=Tr_Time,
                                                     description=Desc).exists()
    return has_transacion


@login_required(login_url='login')
# category view 
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
# transaction view
def transaction(request):
    if 'add_transaction' in request.POST:
        amount = request.POST.get('amount')
        transaction_type = request.POST.get('transactionType')
        transaction_date = request.POST.get('transactionDate')
        transaction_time = request.POST.get('transactionTime')
        transaction_category = request.POST.get('category')
        user_id = request.POST.get('user_id')
        description = request.POST.get('description')
    

        if amount and transaction_type and transaction_date and transaction_time and transaction_category:
            transaction_date = transaction_date.replace('/', '-')
            has_transacion = has_transaction(amount,transaction_time,transaction_date,transaction_category,user_id,transaction_time,description)
            print(has_transacion)
            if has_transacion:
                transaction = Transactions(
                    amount=amount,
                    transaction_type=transaction_type,
                    transaction_date=transaction_date,
                    transaction_time=transaction_time,
                    category_id= Category.objects.get(id=transaction_category, user_id__in=[user_id, 0]),
                    user_id=user_id,
                    description=description
                )
                transaction.save()
                return redirect('add_transactions')
            else:
                messages.error(request,"این تراکنش در سیستم وجود دارد!")
                return redirect('add_transactions')
            
        else:
            messages.error(request, 'All fields are required.')

    transaction_outcome = Transactions.objects.order_by('-transaction_date','-transaction_time').filter(user_id=request.user.id, transaction_type='outcome')
    transaction_income = Transactions.objects.order_by('-transaction_date','-transaction_time').filter(user_id=request.user.id, transaction_type='income')
    category_list = Category.objects.filter(user_id=0) | Category.objects.filter(user_id=request.user.id)

    # Format dates and times for display
    transaction_outcome = [format_date_time(txn) for txn in transaction_outcome]
    transaction_income = [format_date_time(txn) for txn in transaction_income]

    context = {
        'transaction_outcome': transaction_outcome,
        'transaction_income': transaction_income,
        'category': category_list,
    }

    return render(request, 'transactions/transactions.html', context)


@login_required(login_url='login')
def edit_transaction(request):
    if 'edit_transaction' in request.POST:
        transaction_id = request.POST('transaction_id')
        print(f'{transaction_id},edit_transaction')
        # amount = request.POST.get('amount')
        # transaction_type = request.POST.get('transactionType')
        # transaction_date = request.POST.get('transactionDate')
        # transaction_time = request.POST.get('transactionTime')
        # transaction_category = request.POST.get('category')
        # user_id = request.POST.get('user_id')
        # description = request.POST.get('description')

        # transaction_date = transaction_date.replace('/', '-')
        
        # print(amount,transaction_type,transaction_date,transaction_time,transaction_category,user_id,description)
        
        # has_transacion = has_transacion(request,amount,transaction_time,transaction_date,user_id,transaction_category,transaction_time,description)
        # print(has_transacion)
        
        # if has_transacion:
        #     messages.error(request,"این تراکنش در سیستم وجود دارد!")
        #     return redirect('transactions')
    
    return render(request, 'transactions/transactions.html')


@login_required(login_url='login')
def delete_transaction(request):
    if 'delete_transaction' in request.POST:
        transaction_id = request.POST.get('transaction_id')
        print('delete',transaction_id)
        transaction_delete = Transactions.objects.filter(id=transaction_id)
        transaction_delete.delete()

        messages.success(request,"تراکنش با موفقیت حذف شد.")
        return redirect('add_transactions')
    else:
        messages.error(request,"تراکنش با شکست مواجه شد.")
        return redirect('add_transactions')