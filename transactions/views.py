from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from accounts.models import Account
from .models import Transaction
from .serializers import TransferSerializer
from .serializers import TransactionSerializer


class TransferMoneyView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        # 1. Validate request
        serializer = TransferSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        receiver_account_number = serializer.validated_data[
            "receiver_account"
        ]

        amount = serializer.validated_data["amount"]

        # 2. Start database transaction
        with transaction.atomic():  # ⭐ EXISTING - KEEP THIS

            # 3. Get sender's account
            try:
                sender = Account.objects.select_for_update().get(  # ⭐ NEW
                    user=request.user
                )

            except Account.DoesNotExist:
                return Response(
                    {
                        "error": "Sender account not found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            # 4. Check sender is not transferring to himself
            if sender.account_number == receiver_account_number:
                return Response(
                    {
                        "error": "You cannot transfer money to your own account"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 5. Get receiver account
            try:
                receiver = Account.objects.select_for_update().get(  # ⭐ NEW
                    account_number=receiver_account_number
                )

            except Account.DoesNotExist:
                return Response(
                    {
                        "error": "Receiver account not found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            # 6. Check sufficient balance
            if amount > sender.balance:
                return Response(
                    {
                        "error": "Insufficient balance"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 7. Deduct from sender
            sender.balance -= amount
            sender.save()

            # 8. Add to receiver
            receiver.balance += amount
            receiver.save()

            # 9. Create transaction record
            transfer_transaction = Transaction.objects.create(
                account=sender,
                receiver_account=receiver,
                transaction_type="TRANSFER",
                amount=amount,
                balance_after=sender.balance,
                status="SUCCESS"
            )

        # 10. Response
        return Response(
            {
                "message": "Money transferred successfully",
                "transaction_id": transfer_transaction.transaction_id,
                "sender_account": sender.account_number,
                "receiver_account": receiver.account_number,
                "amount": amount,
                "sender_balance_after": sender.balance
            },
            status=status.HTTP_200_OK
        )
class TransactionHistoryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        # Get transactions belonging to logged-in user
        transactions = Transaction.objects.filter(
            account__user=request.user
        ).order_by("-created_at")

        serializer = TransactionSerializer(
            transactions,
            many=True
        )

        return Response(serializer.data)