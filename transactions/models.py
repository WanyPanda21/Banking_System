from django.db import models
from accounts.models import Account


class Transaction(models.Model):

    TRANSACTION_TYPE = [
        ("DEPOSIT", "Deposit"),
        ("WITHDRAW", "Withdraw"),
        ("TRANSFER", "Transfer"),
    ]
    transaction_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    account = models.ForeignKey(                #MANYTOONE
        Account,
        on_delete=models.CASCADE                #"on_delete=models.CASCADE means if the parent object is deleted, Django automatically deletes all related child objects. In my banking project, if an account is deleted, all transactions related to that account are also deleted."
    )

    receiver_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="received_transactions",
        null=True,
        blank=True
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPE
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    balance_after = models.DecimalField(
    max_digits=12,
    decimal_places=2,
    default=0
    )
    status = models.CharField(
        max_length=20,
        default="SUCCESS"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        if not self.transaction_id:
            last_transaction = Transaction.objects.order_by("-id").first()

            if last_transaction:
                number = last_transaction.id + 1
            else:
                number = 1

            self.transaction_id = f"TXN{number:03d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"