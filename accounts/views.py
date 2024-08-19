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
            messages.success(request,'با موفقیت وارد شدید')
            return redirect('index')
        else:
            messages.error(request,"ورود ناموفق")
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
                messages.error(request, 'نام کاربری را وارد کنید')
            elif User.objects.filter(username=username).exists():
                messages.error(request, 'نام کاربری وجود دارد با نام کاربری دیگری امتحان کنید')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'ایمیل وجود دارد با یک ایمیل دیگر ثبت نام کنید')
            else:
                user = User.objects.create_user(username=username,password=password,first_name=firstname,last_name=lastname,email=email)
                user.save()
                messages.success(request,'ثبت نام شما با موفقیت انجام شد')  
                return redirect('index')
        else:
            messages.error(request, 'کلمه عبور مطابقت ندارد') 
    else:
        return render(request,'accounts/signup.html')


def logout_view(request):
    logout(request)
    messages.success(request,"دوباره به ما سر بزنید")
    return redirect('login')