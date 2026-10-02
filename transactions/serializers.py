from rest_framework import serializers
from decimal import Decimal
from .models import Transaction


class DepositSerializer(serializers.Serializer):

    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2
    )
class TransferSerializer(serializers.Serializer):

    receiver_account = serializers.CharField(
        max_length=10
    )

    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0.01")
    )
class TransactionSerializer(serializers.ModelSerializer):

    account_number = serializers.CharField(
        source="account.account_number",
        read_only=True
    )

    account_holder = serializers.CharField(
        source="account.user.username",
        read_only=True
    )

    receiver_account_number = serializers.CharField(
        source="receiver_account.account_number",
        read_only=True,
        allow_null=True
    )

    receiver_name = serializers.CharField(
        source="receiver_account.user.username",
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = Transaction
        fields = [
            "transaction_id",
            "account_number",
            "account_holder",
            "receiver_account_number",
            "receiver_name",
            "transaction_type",
            "amount",
            "balance_after",
            "status",
            "created_at",
        ]