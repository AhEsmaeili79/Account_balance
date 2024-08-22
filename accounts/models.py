from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # Check if the token is still valid (10 minutes)
        return self.created_at >= timezone.now() - timedelta(minutes=10)
    
    def __str__(self):
        return f'{self.user.username}' 