import re
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib import messages,auth
from django.contrib.auth.models import User
from accounts.models import PasswordResetToken
from django.shortcuts import get_object_or_404

token_generator = PasswordResetTokenGenerator()

# validate function
def validate(**kwargs):
    no_error = True

    def add_error(message):
        nonlocal no_error
        request = kwargs['request']
        if request:
            messages.add_message(request, messages.WARNING, message)
        no_error = False

    if 'email' in kwargs and not is_valid_email(kwargs['email']):
        add_error('فرمت ایمیل نامعتبر است')

    if 'firstname' in kwargs and not kwargs['firstname'].isalpha():
        add_error('نام باید فقط شامل حروف باشد')

    if 'lastname' in kwargs and not kwargs['lastname'].isalpha():
        add_error('نام خانوادگی باید فقط شامل حروف باشد')

    if 'password' in kwargs and not is_valid_password(kwargs['password']):
        add_error('رمز عبور باید دارای حروف بزرگ و کوچک و عدد و کاراکتر های خاص باشد')
    
    if 'password_conf' in kwargs and not is_valid_password(kwargs['password_conf']):
        add_error('رمز عبور باید دارای حروف بزرگ و کوچک و عدد و کاراکتر های خاص باشد')
    
    if 'password_conf' in kwargs and 'password' in kwargs and kwargs['password'] != kwargs['password_conf']:
        add_error('رمز عبور باید مطابقت داشته باشد')

    if 'username' in kwargs and not is_valid_username(kwargs['username']):
        add_error('نام کاربری باید با حرف شروع شود و فقط شامل حروف، اعداد و زیرخط باشد')

    return no_error

# validate email
def is_valid_email(email):
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    return re.match(email_pattern, email)

# validate password
def is_valid_password(password):
    return (
        len(password) >= 8 and
        re.search(r'[A-Z]', password) and
        re.search(r'[a-z]', password) and
        re.search(r'\d', password) and
        re.search(r'[!@#\$%\^&\*]', password)
    )

#validate username
def is_valid_username(username):
    return re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', username) and len(username) >= 3

# encode user_io and generate token 
def user_encode(user):
    token = token_generator.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.id))
    PasswordResetToken.objects.create(user=user, token=token)
    return token, uidb64

#decode user_id
def user_decode(uidb64):
    user_id = force_str(urlsafe_base64_decode(uidb64))
    return User.objects.get(id=user_id)


def validate_reset_token(uidb64, token):
    user_id = force_str(urlsafe_base64_decode(uidb64))
    user = get_object_or_404(User, id=user_id)
    
    try:
        token_record = PasswordResetToken.objects.get(user=user, token=token)
    except PasswordResetToken.DoesNotExist:
        return False

    return token_record.is_valid()

# send email function
def SendEmail(request, email, user):
    if is_valid_email(email[0]):
        token, uidb64 = user_encode(user)
        reset_url = request.build_absolute_uri(f'/accounts/reset-password/{uidb64}/{token}/')
        message = build_email_message(user.first_name, reset_url)

        email_message = EmailMessage(
            subject='رمز عبور خود را فراموش کردی؟',
            body=message,
            from_email='test.from.amir@gmail.com',
            to=email,
        )
        email_message.content_subtype = 'html'

        if email_message.send(fail_silently=False):
            messages.success(request, 'پیام با موفقیت ارسال شد در صورت پیدا نکردن اسپم خود را چک کنید')
        else:
            messages.error(request, 'ارسال پیام با شکست مواجه شد')
    else:
        messages.error(request, 'ایمیل به درستی وارد نشده است.')


def register_get_data(req):
    user_data = {
        'username': req.POST.get('userName') or '',
        'firstname': req.POST.get('firstName') or '',
        'lastname': req.POST.get('lastName') or '',
        'email': req.POST.get('email') or '',
        'password': req.POST.get('password') or '',
        'password_conf': req.POST.get('password2') or '',
    }
    return user_data


# build message for email
def build_email_message(first_name, reset_url):
    return f"""
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
            <h1> {first_name} سلام </h1>
            <p>برای تنظیم مجدد کلمه عبور خود، لطفاً بر روی دکمه زیر کلیک کنید:</p>
            <a href="{reset_url}" class="button"><span class="text-button">تنظیم کلمه عبور جدید</span></a>
            <p>اگر شما این درخواست را ارسال نکرده‌اید، لطفاً این ایمیل را نادیده بگیرید.</p>
        </div>
    </body>
    </html>
    """

# Helper functions
def authenticate_user(request, username, password):
    user = auth.authenticate(username=username, password=password)
    if user:
        auth.login(request, user)
        return True
    return False

def create_user(username, firstname, lastname, email, password,password_conf):
    user = User.objects.create_user(username=username, password=password, 
                                    first_name=firstname, last_name=lastname, email=email)
    password_conf = password_conf
    user.save()

def check_user_exists(username, email):
    if User.objects.filter(username=username).exists():
        return 'username_exists'
    elif User.objects.filter(email=email).exists():
        return 'email_exists'
    return None

def send_password_reset_email(request, user):
    SendEmail(request, [user.email], user)

def get_password(req):
    password_data = {
        'password': req.POST.get('password'),
        'password_conf': req.POST.get('password2')
    }
    return password_data


def get_reset_password_date(req,uidb64,token):
    user = user_decode(uidb64)
    password_data = get_password(req)
    password_validate = validate(request=req, **password_data)
    token_validate = validate_reset_token(uidb64, token)
    checked_token = token_generator.check_token(user, token)
    return user,password_data,password_validate,token_validate,checked_token