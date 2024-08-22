from django.urls import path
from .views import LoginPage,SignupPage,logout_view,password_reset

urlpatterns = [
    path('login', LoginPage, name='login'),
    path('signup', SignupPage, name='signup'),
    path('password-reset/',password_reset, name='password_reset'),
    path('logout',logout_view, name='logout'),
]