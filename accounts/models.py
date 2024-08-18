from django.db import models
from django.core.exceptions import ValidationError

def validate_length(value):
    an_integer = value
    a_string = str(an_integer)
    length = len(a_string)
    if length > 10:
        raise ValidationError(
            '%(value)s is above 10 digits'
        )

# Create your models here.
class Account(models.Model):
    username = models.CharField(max_length=150,blank=False)
    first_name = models.CharField(max_length=100,blank=False)
    last_name = models.CharField(max_length=100,blank=False)
    email = models.EmailField(max_length=200,blank=False)
    phone = models.IntegerField(validators=[validate_length],blank=False)
    password = models.IntegerField(validators=[validate_length],blank=False)
    balance = models.DecimalField(max_digits=12,decimal_places=0 ,default=0)
    is_deleted = models.BooleanField(default=1)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'