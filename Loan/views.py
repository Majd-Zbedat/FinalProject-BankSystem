# # from django.shortcuts import render
# #
# # # Create your views here.
# #
# #
# # from rest_framework import generics, status
# # from rest_framework.views import APIView
# #
# # from BankAccount.models import BankAccount
# # from .models import Loan
# # from .serializers import LoanSerializer, GrantLoanSerializer
# # from rest_framework.permissions import IsAuthenticated
# # from BankAccount import models
# # from rest_framework.response import Response
# # from Loan import serializers
# # from django.shortcuts import get_object_or_404
# #
# # views.py
# from django.shortcuts import get_object_or_404
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
#
# import BankAccount
# from BankAccount.serializers import BankAccountSerializer
# from .models import Loan
# from .serializers import GrantLoanSerializer
#
# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from .models import Loan, BankAccount
# from .serializers import GrantLoanSerializer
#
#
# class GrantLoanView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         serializer = GrantLoanSerializer(data=request.data)
#         if serializer.is_valid():
#             account_number = serializer.validated_data['account_number']
#             amount = serializer.validated_data['amount']
#
#             # Check if the account belongs to the logged-in user
#             account = get_object_or_404(BankAccount, account_number=account_number, user=request.user)
#
#             # Proceed with granting the loan
#             loan = Loan.objects.create(account_number=account, amount=amount)
#
#             return Response({"message": "Loan granted successfully.", "loan_id": loan.id},
#                             status=status.HTTP_201_CREATED)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)












from django.shortcuts import render

# Create your views here.


from rest_framework import generics
from .models import Loan
from .serializers import LoanSerializer
from rest_framework.permissions import IsAuthenticated

class LoanCreateView(generics.CreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

class LoanListView(generics.ListAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]









