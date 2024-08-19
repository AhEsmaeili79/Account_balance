from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib import auth

# Create your views here.
def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            messages.success(request,'you are now logged in')
            return redirect('index')
        else:
            messages.error(request,"invalid credential")
            return redirect('login')
    else:
        return render(request,'accounts/login.html')

def SignupPage(request):
    if request.method == 'POST':
        username = request.POST.get('userName')
        firstname = request.POST.get('firstName')
        lastname = request.POST.get('lastName')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('confirmPassword')
        
        if password == password2:
            if not username:
                messages.error(request, 'username cannot be empty.')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'username have already exsits.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'email have already exsits.')
            else:
                user = User.objects.create_user(username=username,password=password,first_name=firstname,last_name=lastname,email=email)
                user.save()
                messages.success(request,'you have regiterd')  
                return redirect('index')
        else:
            messages.error(request, 'Password does not match.') 
    else:
        return render(request,'accounts/signup.html')


def logout_view(request):
    logout(request)
    messages.success(request,"You are logged out")
    return redirect('login')