from django.contrib import admin
from .models import Category,Transactions,Balance

admin.site.register(Category)

admin.site.register(Transactions)
admin.site.register(Balance)
