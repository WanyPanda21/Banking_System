from rest_framework import serializers
from .models import Account


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = [
            "account_number",
            "account_type",
            "balance",
            "status",
            "created_at",
        ]

        read_only_fields = [
            "account_number",
            "balance",
            "status",
            "created_at",
        ]

class DepositSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0.01
    )

class WithdrawSerializer(serializers.Serializer):
    amount = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0.01
    )