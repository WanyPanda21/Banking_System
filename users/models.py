from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('CUSTOMER', 'Customer'),
    )

    phone_number = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CUSTOMER')
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    REQUIRED_FIELDS = ["email", "phone_number"]

    def __str__(self):
        return self.username