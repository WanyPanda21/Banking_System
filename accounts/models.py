from django.db import models                                        # Imports Django's database module.
from django.conf import settings                                    #This imports your Django settings.
import random                                                       #Python's built-in random library. We'll use it to generate a random account number.
 #making a change 

class Account(models.Model):                                        #We use models.Model to create database tables called Account.

    ACCOUNT_TYPE = [
        ("SAVINGS", "Savings"),
        ("CURRENT", "Current"),
    ]

    STATUS = [
        ("ACTIVE", "Active"),
        ("BLOCKED", "Blocked"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,                                    #Use whichever User model is configured in settings.py.
        on_delete=models.CASCADE
    )

    account_number = models.CharField(
        max_length=10,
        unique=True,
        editable=False
    )

    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPE,
        default="SAVINGS"
    )

    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="ACTIVE"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        if not self.account_number:
            self.account_number = str(random.randint(1000000000, 9999999999))

        super().save(*args, **kwargs)

    def __str__(self):
        return self.account_number
