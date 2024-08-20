from django.shortcuts import render
from transactions.models import Balance
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

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