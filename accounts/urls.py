from django.urls import path
from .views import login_page,signup_page,logout_view,forget_password,reset_password

urlpatterns = [
    path('login', login_page, name='login'),
    path('signup', signup_page, name='signup'),
    path('forget-password/',forget_password, name='forget_password'),
    path('reset-password/<uidb64>/<token>/',reset_password, name='reset_password'),
    path('logout',logout_view, name='logout'),
]