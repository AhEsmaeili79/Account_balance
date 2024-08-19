from django.urls import path
from .views import LoginPage,SignupPage,logout_view

urlpatterns = [
    path('login', LoginPage, name='login'),
    path('signup', SignupPage, name='signup'),
    path('logout',logout_view, name='logout'),
]