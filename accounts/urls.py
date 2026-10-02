from django.urls import path
from .views import CreateAccount, MyAccount, DepositMoneyView, WithdrawMoneyView

urlpatterns = [
    path("create/", CreateAccount.as_view(), name="create_account"),
    path("me/", MyAccount.as_view(), name="my_account"),
    path("deposit/", DepositMoneyView.as_view(), name="deposit-money"),
    path("withdraw/",WithdrawMoneyView.as_view(),name="withdraw-money"),
]