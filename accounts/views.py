from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from modules.utils_acc import validate, authenticate_user, create_user, check_user_exists, send_password_reset_email,register_get_data,get_reset_password_date


def login_page(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            user_exists = check_user_exists(username,'')
            password = request.POST.get('password')
            user_is_auth = authenticate_user(request, username, password)

            if user_is_auth:
                messages.success(request, 'با موفقیت وارد شدید')
                return redirect('index')
            elif not user_exists:
                messages.error(request,"نام کاربری مورد نظر وجود ندارد")
                return redirect('login')
            else:
                messages.error(request, "ورود ناموفق")
                return redirect('login')
        
        return render(request, 'accounts/login.html')
    else:
        return redirect('index')


def signup_page(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':

            user_data = register_get_data(request)
            signup_valid = validate(request=request, **user_data)
            user_exists = check_user_exists(user_data['username'], user_data['email'])

            if signup_valid:
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
    else:
            return redirect('index')


def forget_password(request):
    logout_view(request)
    if not request.user.is_authenticated:
        if request.method == 'POST':
            email_or_username = request.POST.get('emailorusername')
            user = User.objects.filter(email=email_or_username).first() or User.objects.filter(username=email_or_username).first()

            if user:
                send_password_reset_email(request, user)
                return redirect('login')
            else:
                messages.error(request, 'ایمیل یا نام کاربری در سیستم وجود ندارد')
        
        return render(request, 'accounts/forget_password.html')
    else:
        messages.error(request, 'برای ثبت درخواست ابتدا باید از اکانت خود خارج شوید.')
        return redirect('index')


def reset_password(request, uidb64, token):
    if not request.user.is_authenticated:
        if request.method == "POST":
            try:
                user,password_data,password_validate,token_validate,checked_token = get_reset_password_date(request,uidb64,token)
                if token_validate > 0:
                    if checked_token:
                        if password_validate:
                            user.set_password(password_data['password'])
                            user.save()
                            messages.success(request, 'کلمه عبور با موفقیت تغییر کرد')
                            return redirect('login')
                    else:
                        messages.error(request, "دوباره تلاش کنید")
                else: 
                    messages.error(request, "زمان تغییر کلمه عبور به اتمام رسید دوباره درخواست دهید")
            
            except User.DoesNotExist:
                messages.error(request, 'کاربری با این اطلاعات وجود ندارد')
                return redirect('forget_password')

        return render(request, 'accounts/reset_password.html')
    else:
            messages.error(request, 'برای تغییر کلمه عبور باید از اکانت خود خارج شوید.')
            return redirect('index')

def arabic_to_latin_number(text):
    arabic_to_latin_map = str.maketrans('٠١٢٣٤٥٦٧٨٩', '0123456789')
    return text.translate(arabic_to_latin_map)


@login_required(login_url='login')
def update_profile(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        userdata = {
            "firstname" : request.POST.get('first_name') or "",
            "lastname" : request.POST.get('last_name') or "",
            "email" : arabic_to_latin_number(request.POST.get('email')) or "",
        }

        user_inf = User.objects.filter(id=user_id)
        for i in user_inf:
            email_user = i.email
        
        user_exists = check_user_exists('', userdata["email"])
        update_valid = validate(request=request, **userdata)
        
    
        if update_valid:
            if not user_exists or email_user == userdata['email'] :
                user = get_object_or_404(User,id=user_id)
                user.first_name = userdata["firstname"]
                user.last_name = userdata["lastname"]
                user.email = userdata["email"]
                user.save()
                messages.success(request,"اطلاعات با موفقیت تغییر کرد")
                return redirect('update_profile')
            else:
                messages.error(request,"این ایمیل قبلا استفاده شده است.")
                return redirect('update_profile')
        else:
            return redirect('update_profile')
            

    return render(request,'accounts/update-profile.html')


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.success(request, "دوباره به ما سر بزنید")
    return redirect('login')
