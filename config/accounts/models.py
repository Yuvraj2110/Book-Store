# accounts/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    is_cashier = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    phone = models.CharField(max_length=40, blank=True)

    def __str__(self):
        return self.user.get_username()


class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile', null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    loyalty_points = models.IntegerField(default=0)

    def __str__(self):
        return self.name
