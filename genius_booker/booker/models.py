from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Store(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    opening_days = models.JSONField()  # To store opening days as a list
    start_time = models.TimeField()
    end_time = models.TimeField()
    lunch_start_time = models.TimeField()
    lunch_end_time = models.TimeField()
    subscribe = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Staff(AbstractUser):
    phone = models.CharField(max_length=15)
    active = models.BooleanField(default=False)
    role = models.CharField(max_length=255)
    schedule = models.JSONField()  # To store staff schedule details
    stores = models.ManyToManyField(Store, related_name='staff')

    # Avoid naming conflicts with Django’s User model
    groups = models.ManyToManyField(
        Group,
        related_name='staff_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='staff_set',
        blank=True,
    )

    def __str__(self):
        return self.username
