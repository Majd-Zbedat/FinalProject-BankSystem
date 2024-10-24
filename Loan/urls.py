# from django.urls import path
# from . import views
# from .views import GrantLoanView
#
# urlpatterns = [
#     #path('grant', views.GrantLoanView.as_view(), name='grant-loan'),
#     # path('repayment/', views.LoanRepaymentView.as_view(), name='loan-repayment'),
#     # path('customer-loans/',views.GetCustomerLoansView.as_view(), name='customer-loans'),
#     path('grant/', views.GrantLoanView.as_view(), name='grant_loan'),
# ]


from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.LoanCreateView.as_view(), name='create-loan'),
    path('list/', views.LoanListView.as_view(), name='loan-list'),
]
