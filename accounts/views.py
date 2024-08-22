from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.models import User

from modules.func import user_decode, validate, authenticate_user, create_user, check_user_exists, send_password_reset_email

token_generator = PasswordResetTokenGenerator()

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if authenticate_user(request, username, password):
            messages.success(request, 'با موفقیت وارد شدید')
            return redirect('index')
        else:
            messages.error(request, "ورود ناموفق")
            return redirect('login')
    
    return render(request, 'accounts/login.html')

def signup_page(request):
    if request.method == 'POST':
        user_data = {
            'username': request.POST.get('userName') or '',
            'firstname': request.POST.get('firstName') or '',
            'lastname': request.POST.get('lastName') or '',
            'email': request.POST.get('email') or '',
            'password': request.POST.get('password') or '',
            'password_conf': request.POST.get('password2') or '',
        }

        if validate(request=request, **user_data):
            user_exists = check_user_exists(user_data['username'], user_data['email'])
            if user_exists == 'username_exists':
                messages.error(request, 'نام کاربری وجود دارد با نام کاربری دیگری امتحان کنید')
            elif user_exists == 'email_exists':
                messages.error(request, 'ایمیل وجود دارد با یک ایمیل دیگر ثبت نام کنید')
            else:
                create_user(**user_data)
                messages.success(request, 'ثبت نام شما با موفقیت انجام شد')
                return redirect('login')

        return redirect('signup')
    
    return render(request, 'accounts/signup.html')

def forget_password(request):
    if request.method == 'POST':
        email_or_username = request.POST.get('emailorusername')
        user = User.objects.filter(email=email_or_username).first() or User.objects.filter(username=email_or_username).first()

        if user:
            send_password_reset_email(request, user)
            return redirect('login')
        else:
            messages.error(request, 'ایمیل یا نام کاربری در سیستم وجود ندارد')
    
    return render(request, 'accounts/forget_password.html')

def reset_password(request, uidb64, token):
    if request.method == "POST":
        try:
            user = user_decode(uidb64)
            if token_generator.check_token(user, token):
                password_data = {
                    'password': request.POST.get('password'),
                    'password2': request.POST.get('password2')
                }

                if validate(request=request, **password_data):
                    user.set_password(password_data['password'])
                    user.save()
                    messages.success(request, 'کلمه عبور با موفقیت تغییر کرد')
                    return redirect('login')
            else:
                messages.error(request, 'تغییر کلمه عبور شما با مشکل مواجه شد دوباره درخواست دهید')
                return redirect('forget_password')
        except User.DoesNotExist:
            messages.error(request, 'کاربری با این اطلاعات وجود ندارد')
            return redirect('forget_password')

    return render(request, 'accounts/reset_password.html')

def logout_view(request):
    logout(request)
    messages.success(request, "دوباره به ما سر بزنید")
    return redirect('login')
