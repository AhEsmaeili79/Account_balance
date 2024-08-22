from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib import auth
from django.core.mail import send_mail
import re


def SendEmail(req,email,user):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.fullmatch(regex,email[0]):
                send_mail(
                        subject= 'رمز عبور خود را فراموش کردی؟',
                        message= f'سلام {user}',
                        from_email='test.from.amir@gmail.com',
                        recipient_list= email,
                        fail_silently=False,
                    )
                if send_mail:
                    messages.success(req,' پیام با موفقیت ارسال شد در صورت پیدا نکردن اسپم خود را چک کنید')
                else:
                    messages.error(req,'ارسال پیام با شکست مواجه شد')




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
    
    
def password_reset(request):
    if 'emailorusername' in request.POST:
        EmailorUser = request.POST.get('emailorusername')
        email_exist = User.objects.filter(email=EmailorUser).exists()
        username_exist = User.objects.filter(username=EmailorUser).exists()

        if email_exist:
            user = User.objects.get(email=EmailorUser)
            SendEmail(request,[EmailorUser],user.username)
        elif username_exist:
            user = User.objects.get(username=EmailorUser)
            SendEmail(request,[user.email],EmailorUser)
        else:
            messages.error(request,'ایمیل در سیستم وجود ندارد')

    return render(request,'accounts/forget_password.html')

def logout_view(request):
    logout(request)
    messages.success(request,"دوباره به ما سر بزنید")
    return redirect('login')