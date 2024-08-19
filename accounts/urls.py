from django.urls import path
from .views import LoginPage,SignupPage

urlpatterns = [
    path('login', LoginPage, name='login'),
    path('signup', SignupPage, name='signup'),
]