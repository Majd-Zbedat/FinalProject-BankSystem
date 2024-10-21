from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.TransactionCreateView.as_view(), name='create-transaction'),
    path('list/', views.TransactionListView.as_view(), name='transaction-list'),
]
