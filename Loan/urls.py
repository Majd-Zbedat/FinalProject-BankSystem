from django.urls import path
from . import views
# Loan/urls.py
from django.urls import path
from .views import GrantLoanView, LoanListView

urlpatterns = [
    path('grant/', GrantLoanView.as_view(), name='grant-loan'),
     path('list/', LoanListView.as_view(), name='loan-list'),
    # path('list/', LoanListView.as_view(), name='loan-list'),
    path('repay/', views.RepayLoanView.as_view(), name='repay-loan'),
]
