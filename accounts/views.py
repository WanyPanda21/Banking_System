from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Account
from .serializers import AccountSerializer
from .serializers import DepositSerializer
from .serializers import WithdrawSerializer
from transactions.models import Transaction

#making changes xyz
#making another changes
class CreateAccount(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Create a new account for the logged-in user.
        
        """

        # Check if the user already has an account
        if Account.objects.filter(user=request.user).exists():
            return Response(
                {
                    "error": "Account already exists."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = AccountSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save(user=request.user)

            return Response(
                {
                    "message": "Account created successfully.",
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
class MyAccount(APIView):

    permission_classes = [IsAuthenticated]                      #Only logged-in users can access it.
    def get(self, request):
        account = Account.objects.get(user=request.user)       #Get the Account whose user is the currently logged-in user.-> request.user = john  -> Account.objects.get(user=john)
        serializer = AccountSerializer(account)                 #coverts to json

        return Response(serializer.data)


class DepositMoneyView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        # Validate request data
        serializer = DepositSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get logged-in user's account
        account = Account.objects.get(user=request.user)

        # Get deposit amount
        amount = serializer.validated_data["amount"]

        # Update balance
        account.balance += amount
        account.save()
        transaction = Transaction.objects.create(
        account=account,
        transaction_type="DEPOSIT",
        amount=amount,
        status="SUCCESS"
    )

        return Response(
            {
                "message": "Money deposited successfully",
                "account_number": account.account_number,
                "deposited_amount": amount,
                "new_balance": account.balance
            },
            status=status.HTTP_200_OK
        )




class WithdrawMoneyView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        # 1. Validate amount
        serializer = WithdrawSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. Get logged-in user's account
        account = Account.objects.get(user=request.user)

        # 3. Get withdrawal amount
        amount = serializer.validated_data["amount"]

        # 4. Check sufficient balance
        if amount > account.balance:
            return Response(
                {
                    "error": "Insufficient balance"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # 5. Deduct money
        account.balance -= amount

        # 6. Save updated balance
        account.save()
        transaction = Transaction.objects.create(
        account=account,
        transaction_type="WITHDRAW",
        amount=amount,
        status="SUCCESS"
    )
        # 7. Return response
        return Response(
            {
                "message": "Money withdrawn successfully",
                "account_number": account.account_number,
                "withdrawn_amount": amount,
                "remaining_balance": account.balance
            },
            status=status.HTTP_200_OK
        )

class AccountBalanceView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        account = Account.objects.get(user=request.user)

        return Response(
            {
                "account_number": account.account_number,
                "balance": account.balance
            },
            status=status.HTTP_200_OK
        )
