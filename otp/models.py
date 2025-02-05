from django.db import models
from django.contrib.auth.models import User


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField()

    def __str__(self):
        return f"OTP for {self.user.username}"
