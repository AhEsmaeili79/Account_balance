from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def LoginPage(request):
    if User.is_authenticated == "":
        messages.error(request, 'You have already LoggedIn.')
        return redirect(request,'index')
    else:
        return render(request,'accounts/login.html')

def SignupPage(request):
    if User.is_authenticated == "":
        messages.error(request, 'You have already SignedUp.')
        return redirect(request,'index')
    else:
        return render(request,'accounts/signup.html')