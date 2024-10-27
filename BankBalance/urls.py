from django.urls import path
from .views import BankBalanceView

urlpatterns = [
    path('balance/', BankBalanceView.as_view(), name='bank-balance'),  # URL for accessing bank balance
]
