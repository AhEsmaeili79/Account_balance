from django.urls import path
from .views import login_page,signup_page,logout_view,forget_password,reset_password,update_profile

urlpatterns = [
    path('login', login_page, name='login'),
    path('signup', signup_page, name='signup'),
    path('forget-password',forget_password, name='forget_password'),
    path('reset-password/<uidb64>/<token>/',reset_password, name='reset_password'),
    path('update-profile',update_profile,name = 'update_profile'),
    path('logout',logout_view, name='logout'),
]