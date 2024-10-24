from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.BankAccountCreateView.as_view(), name='create-bank-account'),
    path('list/', views.BankAccountListView.as_view(), name='list-bank-accounts'),
    path('suspend/', views.BankAccountSuspendUnsuspendView.as_view(), name='bank-account-suspend'),
    path('status/', views.BankAccountStatusView.as_view(), name='bank-account-suspend'), #status of the account if it's Active or not
    path('deposit/', views.DepositView.as_view(), name='bank-account-deposit'), #Last change
    path('withdraw/', views.WithdrawView.as_view(), name='bank-account-withdraw'),
    path('get-balance/', views.GetBalanceView.as_view(), name='bank-account-get-balance'),
    path('get-balance/', views.GetBalanceView.as_view(), name='bank-account-get-balance'),
    path('transfer/', views.TransferView.as_view(), name='bank-account-transfer'),

]
