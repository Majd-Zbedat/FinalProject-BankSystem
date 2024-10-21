from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.LoanCreateView.as_view(), name='create-loan'),
    path('list/', views.LoanListView.as_view(), name='loan-list'),
]
