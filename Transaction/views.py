# from django.shortcuts import render
#
# # Create your views here.
#
#
# from rest_framework import generics
# from .models import Transaction
# from .serializers import TransactionSerializer
# from rest_framework.permissions import IsAuthenticated
#
# from rest_framework import generics
# from .models import Transaction
# from .serializers import TransactionSerializer
# from rest_framework.permissions import IsAuthenticated
#
# class CustomerTransactionListView(generics.ListAPIView):
#     serializer_class = TransactionSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         # Return only the transactions of the authenticated user
#         return Transaction.objects.filter(user=self.request.user)
