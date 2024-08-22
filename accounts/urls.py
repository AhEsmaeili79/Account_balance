from django.urls import path
from .views import LoginPage,SignupPage,logout_view,forget_password,reset_password

urlpatterns = [
    path('login', LoginPage, name='login'),
    path('signup', SignupPage, name='signup'),
    path('forget-password/',forget_password, name='forget_password'),
    path('reset-password/<uidb64>/<token>/',reset_password, name='reset_password'),
    path('logout',logout_view, name='logout'),
]