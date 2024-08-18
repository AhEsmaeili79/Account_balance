from django.db import models
from persian_datetime.utils import get_persian_datetime
from accounts.models import User

persian_date, persian_time = get_persian_datetime()


class Category(models.Model):
    category_name = models.CharField(max_length=100,blank=False)
    
    def __str__(self):
        return self.category_name

# Create your models here.
class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('outcome', 'Outcome'),
    )
    amount = models.IntegerField(default=0,max_length=1000000000,blank=False)
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPES,default="Income",blank=False)
    transaction_date = models.DateTimeField(default=persian_date)
    transaction_time = models.TimeField(default=persian_time)
    account_id = models.ForeignKey(User,on_delete=models.CASCADE,related_name='transactions')
    category_id = models.ForeignKey(Category,on_delete=models.DO_NOTHING)
    description = models.TextField(max_length=300,blank=True)

    def __str__(self):
        return f'{self.transaction_type.capitalize()} - {self.amount} on {self.transaction_date}'