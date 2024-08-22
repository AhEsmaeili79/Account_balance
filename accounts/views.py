from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib import auth
from django.core.mail import EmailMessage
from django.utils.encoding import force_str,force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import re

token_generator = PasswordResetTokenGenerator()





def SendEmail(req,email,user):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.fullmatch(regex,email[0]):
        token = token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        reset_url = req.build_absolute_uri(f'/accounts/reset-password/{uidb64}/{token}/')

        subject = 'رمز عبور خود را فراموش کردی؟'
        message = f"""
        <!DOCTYPE html>
        <html lang="fa">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                @font-face {{
                    font-family: 'B Yekan';
                    src: url('https://github.com/mrlco/persian-web-fonts/blob/master/fonts/BYekan.ttf') format('truetype');
                    font-weight: normal;
                    font-style: normal;
                }}
                body {{
                    font-family: 'B Yekan', Arial, sans-serif;
                    background-color: #f4f4f4;
                    color: #333;
                    text-align: center;
                    padding: 20px;
                }}
                .container {{
                    background-color: #ffffff;
                    font-family: 'B Yekan', Arial, sans-serif;
                    border-radius: 8px;
                    padding: 20px;
                    max-width: 600px;
                    margin: 0 auto;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                h1 {{
                    font-family: 'B Yekan', Arial, sans-serif;
                    font-size: 24px;
                    margin-bottom: 20px;
                }}
                p {{
                    font-family: 'B Yekan', Arial, sans-serif;
                    font-size: 25px;
                    line-height: 1.5;
                }}
                .button {{
                    display: inline-block;
                    font-size: 20px;
                    color:#fff;
                    background-color: #007bff;
                    padding: 15px 30px;
                    text-decoration: none;
                    border-radius: 5px;
                    margin-top: 20px;
                    font-family: 'B Yekan', Arial, sans-serif;
                }}
                .button:hover {{
                    background-color: #0056b3;
                    color:#fff;
                }}
                .ii a[href] {{
                    color: #fff;
                }}
                .text-button{{
                    color: #fff;
                }}
                a {{
                    color: #007bff; /* Set the color of the link */
                    text-decoration: none; /* Remove underline */
                }}
                a:visited {{
                    color: #007bff; /* Set the color for visited links */
                }}
                a:hover {{
                    color: #0056b3; /* Set the color when hovering over the link */
                    text-decoration: none; /* Ensure underline is not added on hover */
                }}
                a:active {{
                    color: #0056b3; /* Set the color for active links */
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1> {user.first_name } سلام </h1>
                <p>برای تنظیم مجدد کلمه عبور خود، لطفاً بر روی دکمه زیر کلیک کنید:</p>
                <a href="{reset_url}" class="button"><span class="text-button">تنظیم کلمه عبور جدید</span></a>
                <p>اگر شما این درخواست را ارسال نکرده‌اید، لطفاً این ایمیل را نادیده بگیرید.</p>
            </div>
        </body>
        </html>
        """

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email='test.from.amir@gmail.com',
            to = email,
        )
        email.content_subtype = 'html'  # Important to set the email type as HTML
        email.send(fail_silently=False)
        if email:
            messages.success(req,' پیام با موفقیت ارسال شد در صورت پیدا نکردن اسپم خود را چک کنید')
            return redirect('login')
        else:
            messages.error(req,'ارسال پیام با شکست مواجه شد')
            return redirect('login')


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
    
    
def forget_password(request):
    if 'emailorusername' in request.POST:
        EmailorUser = request.POST.get('emailorusername')
        email_exist = User.objects.filter(email=EmailorUser).exists()
        username_exist = User.objects.filter(username=EmailorUser).exists()

        if email_exist:
            user = User.objects.get(email=EmailorUser)
            SendEmail(request,[EmailorUser],user)
            return redirect('login')
        elif username_exist:
            user = User.objects.get(username=EmailorUser)
            SendEmail(request,[user.email],user)
            return redirect('login')
        else:
            messages.error(request,'ایمیل در سیستم وجود ندارد')

    return render(request,'accounts/forget_password.html')


def reset_password(request,uidb64,token):
    if request.method == "POST":
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            
            if token_generator.check_token(user,token):
                new_pass = request.POST.get('password')
                new_pass2 = request.POST.get('password2')
                if new_pass == new_pass2:
                    user.set_password(new_pass)
                    user.save()
                    
                    messages.success(request,'کلمه عبور با موفقیت تغییر کرد')
                    return redirect('login')
                
                else:
                    messages.error(request,'کلمه عبور با هم مطابقت ندارد')

            else:
                messages.error(request,'تغییر کلمه عبور شما با مشکل مواجه شد دوباره درخواست دهید')
                return redirect('forget_password')
            
        except User.DoesNotExist:
            messages.error(request,'کاربری با این اطلاعات وجود ندارد')
            return redirect('forget_password')
        
    return render(request,'accounts/reset_password.html')

def logout_view(request):
    logout(request)
    messages.success(request,"دوباره به ما سر بزنید")
    return redirect('login')