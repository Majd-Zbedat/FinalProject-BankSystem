<<<<<<< HEAD
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
=======
from rest_framework import generics
from .serializers import TransactionSerializer





from rest_framework.views import APIView
from rest_framework.response import Response
from Transaction.models import Transaction

from rest_framework.permissions import IsAuthenticated


class TransactionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_superuser:
            transactions = Transaction.objects.all()
        else:
            transactions = Transaction.objects.filter(user=request.user)

        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)









class AccountOperationsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_superuser:
            transactions = Transaction.objects.all()  # Superusers see all transactions
        else:
            transactions = Transaction.objects.filter(user=request.user)

        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)







>>>>>>> 2b87986d (Last Version Of Project)
