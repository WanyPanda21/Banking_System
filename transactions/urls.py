from django.urls import path
from .views import TransferMoneyView, TransactionHistoryView


urlpatterns = [
    path("transfer/",TransferMoneyView.as_view(),name="transfer-money"),
    path("TransactionHistoryView/",TransactionHistoryView.as_view(),name="transaction-history"),
]