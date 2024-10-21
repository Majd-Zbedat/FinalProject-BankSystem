from django.shortcuts import render

# Create your views here.
from rest_framework import generics

from User.serializers import UserSerializer, User
from .models import BankAccount
from .serializers import BankAccountSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import BankAccount
from .serializers import BankAccountSerializer  # Assuming you have an appropriate serializer




class BankAccountCreateView(generics.CreateAPIView):

    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated]

class BankAccountListView(generics.ListAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated]




# class BankAccountListView(APIView):
#     def get(self, request):
#         bank_accounts = BankAccount.objects.all()
#         serializer = BankAccountSerializer(bank_accounts, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request, account_number):
#         # Update the suspended status
#         bank_account = get_object_or_404(BankAccount, account_number=account_number)
#         suspended_status = request.data.get('suspended')
#
#         # Ensure the account can be suspended only if the balance is not negative
#         if suspended_status is not None:
#             if suspended_status and bank_account.balance < 0:
#                 return Response({"error": "Cannot suspend an account with negative balance."}, status=status.HTTP_400_BAD_REQUEST)
#
#             bank_account.suspended = suspended_status
#             bank_account.save()
#             return Response({"message": "Account suspension status updated."}, status=status.HTTP_200_OK)
#
#         return Response({"error": "Invalid request data."}, status=status.HTTP_400_BAD_REQUEST)
#

#####################################################################################################################################
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.shortcuts import get_object_or_404
# from .models import BankAccount
# from .serializers import BankAccountSerializer
#
# class BankAccountSuspendView(APIView):
#     def get(self, request):
#         # List all bank accounts for selection
#         accounts = BankAccount.objects.all()
#         serializer = BankAccountSerializer(accounts, many=True)
#         return Response(serializer.data)
#
#     def put(self, request):
#         account_number = request.data.get('account_number')
#
#         # Check if account number is provided
#         if not account_number:
#             return Response({"error": "Account number is required."}, status=status.HTTP_400_BAD_REQUEST)
#
#         # Retrieve the bank account by account_number
#         bank_account = get_object_or_404(BankAccount, account_number=account_number)
#
#         # Check if the balance is negative
#         if bank_account.balance < 0:
#             return Response({"error": "Cannot suspend an account with a negative balance."}, status=status.HTTP_400_BAD_REQUEST)
#
#         # Update the suspended status
#         bank_account.suspended = True  # Set suspended to True
#         bank_account.save()
#
#         return Response({"message": "Account suspended successfully."}, status=status.HTTP_200_OK)

##################################################################################################################################





#
#
#
#
# class BankAccountSuspendView(APIView):
#     def post(self, request):
#         account_number = request.data.get('account_number')  # Get the account number from request
#         bank_account = get_object_or_404(BankAccount, account_number=account_number)
#
#         # Check if the balance is negative
#         if bank_account.balance < 0:
#             return Response({"error": "Cannot suspend the account with a negative balance."}, status=status.HTTP_400_BAD_REQUEST)
#
#         # Suspend the account
#         bank_account.is_suspended = True
#         bank_account.save()
#
#         return Response({"message": "Bank account suspended successfully."}, status=status.HTTP_200_OK)





#
# class BankAccountSuspendView(APIView):
#     def get(self, request):
#         # List all bank accounts for selection
#         accounts = BankAccount.objects.all()  # Retrieve all bank accounts
#         serializer = BankAccountSerializer(accounts, many=True)
#         return Response(serializer.data)
#
#     def put(self, request, account_number):
#         # Retrieve the bank account
#         bank_account = get_object_or_404(BankAccount, account_number=account_number)
#
#         # Check if the balance is negative
#         if bank_account.balance < 0:
#             return Response({"error": "Cannot suspend an account with a negative balance."}, status=status.HTTP_400_BAD_REQUEST)
#
#         # Update the suspended status
#         bank_account.suspended = True  # Set suspended to True
#         bank_account.save()
#
#         return Response({"message": "Account suspended successfully."}, status=status.HTTP_200_OK)









class BankAccountSuspendUnsuspendView(APIView):
    def get(self, request):
        # List all bank accounts for selection
            accounts = BankAccount.objects.all()
            serializer = BankAccountSerializer(accounts, many=True)
            return Response(serializer.data)

    def put(self, request):
        account_number = request.data.get('account_number')
        action = request.data.get('action')  # Expecting 'suspend' or 'unsuspend'

        # Check if account number is provided
        if not account_number:
            return Response({"error": "Account number is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the bank account by account_number
        bank_account = get_object_or_404(BankAccount, account_number=account_number)

        if action == 'suspend':
            if bank_account.balance < 0:
                return Response({"error": "Cannot suspend an account with a negative balance."}, status=status.HTTP_400_BAD_REQUEST)
            bank_account.suspended = True
            bank_account.save()
            return Response({"message": "Account suspended successfully."}, status=status.HTTP_200_OK)

        elif action == 'unsuspend':
            if not bank_account.suspended:
                return Response({"error": "Account is already active. The balance is negative!"}, status=status.HTTP_400_BAD_REQUEST)
            bank_account.suspended = False
            bank_account.save()
            return Response({"message": "Account unsuspended successfully."}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)


class BankAccountStatusView(APIView):
    def get(self, request):
        # List all bank accounts for selection
            accounts = BankAccount.objects.all()
            serializer = BankAccountSerializer(accounts, many=True)
            return Response(serializer.data)

    def put(self, request):
        account_number = request.data.get('account_number')
        action = request.data.get('action')  # Expecting 'block' or 'activate'

        # Check if account number is provided
        if not account_number:
            return Response({"error": "Account number is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the bank account by account_number
        bank_account = get_object_or_404(BankAccount, account_number=account_number)

        if action == 'block':
            bank_account.status = 'blocked'
            bank_account.save()
            return Response({"message": "Account blocked successfully."}, status=status.HTTP_200_OK)

        elif action == 'activate':
            if bank_account.status != 'blocked':
                return Response({"error": "Account is not blocked."}, status=status.HTTP_400_BAD_REQUEST)
            bank_account.status = 'active'
            bank_account.save()
            return Response({"message": "Account activated successfully."}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)





