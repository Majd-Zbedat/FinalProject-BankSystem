from django.core.exceptions import PermissionDenied
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



##########################################
def is_account_owner(user, account):
    return account.user == user


###########################################
#
# class BankAccountCreateView(generics.CreateAPIView):
#
#     queryset = BankAccount.objects.all()
#     serializer_class = BankAccountSerializer
#     permission_classes = [IsAuthenticated]

# class BankAccountListView(generics.ListAPIView):
#     #queryset = BankAccount.objects.all()
#
#     serializer_class = BankAccountSerializer
#     permission_classes = [IsAuthenticated]


from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import BankAccount
from .serializers import BankAccountSerializer


class BankAccountCreateView(generics.CreateAPIView):
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Check if the user is a superuser
        if not self.request.user.is_superuser:
            raise PermissionDenied("You do not have permission to create a bank account.")

        # Save the bank account if the user is a superuser
        serializer.save()





class BankAccountListView(generics.ListAPIView):
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Check if the user is a superuser
        if self.request.user.is_superuser:
            # Superusers can see all bank accounts
            return BankAccount.objects.all()
        else:
            # Regular users can only see their own bank accounts
            return BankAccount.objects.filter(user=self.request.user)





##### Last change in 9:38

# class BankAccountSuspendUnsuspendView(APIView):
#     def get(self, request):
#             accounts = BankAccount.objects.all()
#             serializer = BankAccountSerializer(accounts, many=True)
#             return Response(serializer.data)
#
#     def put(self, request):
#         account_number = request.data.get('account_number')
#         action = request.data.get('action')  # Expecting 'suspend' or 'unsuspend'
#
#         if not account_number:
#             return Response({"error": "Account number is required."}, status=status.HTTP_400_BAD_REQUEST)
#
#         bank_account = get_object_or_404(BankAccount, account_number=account_number)
#
#         if action == 'suspend':
#             if bank_account.balance < 0:
#                 return Response({"error": "Cannot suspend an account with a negative balance."}, status=status.HTTP_400_BAD_REQUEST)
#             bank_account.suspended = True
#             bank_account.save()
#             return Response({"message": "Account suspended successfully."}, status=status.HTTP_200_OK)
#
#         elif action == 'unsuspend':
#             if not bank_account.suspended:
#                 return Response({"error": "Account is already active. The balance is negative!"}, status=status.HTTP_400_BAD_REQUEST)
#             bank_account.suspended = False
#             bank_account.save()
#             return Response({"message": "Account unsuspended successfully."}, status=status.HTTP_200_OK)
#
#         return Response({"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)




from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import BankAccount
from .serializers import BankAccountSerializer  # Assuming you have this serializer

# class BankAccountSuspendUnsuspendView(APIView):
#     def get(self, request):
#         if request.user.is_superuser:
#             accounts = BankAccount.objects.all()
#         else:
#             accounts = BankAccount.objects.filter(user=request.user)
#
#         serializer = BankAccountSerializer(accounts, many=True)
#         return Response(serializer.data)

    # def put(self, request):
    #     # Check if the user is a superuser
    #     if not request.user.is_superuser:
    #         return Response({"error": "Only super users can suspend or unsuspend accounts."}, status=status.HTTP_403_FORBIDDEN)
    #
    #     account_number = request.data.get('account_number')
    #     action = request.data.get('action')  # Expecting 'suspend' or 'unsuspend'
    #
    #     if not account_number:
    #         return Response({"error": "Account number is required."}, status=status.HTTP_400_BAD_REQUEST)
    #
    #     bank_account = get_object_or_404(BankAccount, account_number=account_number)
    #
    #     if action == 'suspend':
    #         if bank_account.balance < 0:
    #             return Response({"error": "Cannot suspend an account with a negative balance."}, status=status.HTTP_400_BAD_REQUEST)
    #         bank_account.suspended = True
    #         bank_account.save()
    #         return Response({"message": "Account suspended successfully."}, status=status.HTTP_200_OK)
    #
    #     elif action == 'unsuspend':
    #         if not bank_account.suspended:
    #             return Response({"error": "Account is already active."}, status=status.HTTP_400_BAD_REQUEST)
    #         bank_account.suspended = False
    #         bank_account.save()
    #         return Response({"message": "Account unsuspended successfully."}, status=status.HTTP_200_OK)
    #
    #     return Response({"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)

class BankAccountSuspendUnsuspendView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
            if request.user.is_superuser:
                accounts = BankAccount.objects.all()
            else:
                accounts = BankAccount.objects.filter(user=request.user)

            serializer = BankAccountSerializer(accounts, many=True)
            return Response(serializer.data)

    def put(self, request):
        account_number = request.data.get('account_number')
        action = request.data.get('action')  # Expecting 'suspend' or 'unsuspend'

        if not account_number:
            return Response({"error": "Account number is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the account using the account number
        bank_account = get_object_or_404(BankAccount, account_number=account_number)

        # Superuser can suspend/unsuspend any account, regular user only their own account
        if not request.user.is_superuser and bank_account.user != request.user:
            return Response({"error": "You are only allowed to suspend/unsuspend your own accounts."}, status=status.HTTP_403_FORBIDDEN)

        # Check if the account is blocked; a blocked account cannot be suspended
        if bank_account.status == 'blocked':
            return Response({"error": "Your account is blocked can't be suspend/unsuspend!."}, status=status.HTTP_400_BAD_REQUEST)

        if action == 'suspend':
            # Check if the balance is negative
            if bank_account.balance < 0:
                return Response({"error": "Cannot suspend an account with a negative balance."}, status=status.HTTP_400_BAD_REQUEST)
            bank_account.suspended = True
            bank_account.save()
            return Response({"message": "Account suspended successfully."}, status=status.HTTP_200_OK)

        elif action == 'unsuspend':
            if not bank_account.suspended:
                return Response({"error": "Account is already active."}, status=status.HTTP_400_BAD_REQUEST)
            bank_account.suspended = False
            bank_account.save()
            return Response({"message": "Account unsuspended successfully."}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)























class BankAccountStatusView(APIView):
    def get(self, request):
        if request.user.is_superuser:
            accounts = BankAccount.objects.all()
        else:
            accounts = BankAccount.objects.filter(user=request.user)

        serializer = BankAccountSerializer(accounts, many=True)
        return Response(serializer.data)

    def put(self, request):
        if not request.user.is_superuser:
            return Response({"error": "Only super users can block or active accounts."}, status=status.HTTP_403_FORBIDDEN)

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

        elif action == 'active':
            if bank_account.status != 'blocked':
                return Response({"error": "Account is not blocked."}, status=status.HTTP_400_BAD_REQUEST)
            bank_account.status = 'active'
            bank_account.save()
            return Response({"message": "Account activated successfully."}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)


from .serializers import BankAccountSerializer

##############################################################3
# class DepositView(APIView):
#     def get(self, request):
#         # List all bank accounts for selection
#             accounts = BankAccount.objects.all()
#             serializer = BankAccountSerializer(accounts, many=True)
#             return Response(serializer.data)
#     def post(self, request):
#         serializer = BankAccountSerializer(data=request.data)
#         if serializer.is_valid():
#             account_number = serializer.validated_data['account_number']
#             amount = serializer.validated_data['amount']
#             account = get_object_or_404(BankAccount, account_number=account_number)
#
#             account.balance += amount
#             account.save()
#
#             return Response({"message": "Deposit successful", "new_balance": account.balance},
#                             status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #


from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import BankAccount
from .serializers import BankAccountSerializer, \
    BankAccountDepositSerializer  # Ensure you have a separate serializer for deposits


class DepositView(APIView):
    permission_classes = [IsAuthenticated]  # Only authenticated users can access this view

    def get(self, request):
        # List only the bank accounts of the authenticated user
        accounts = BankAccount.objects.filter(user=request.user)
        serializer = BankAccountSerializer(accounts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BankAccountDepositSerializer(data=request.data)
        if serializer.is_valid():
            account_number = serializer.validated_data['account_number']
            amount = serializer.validated_data['amount']

            # Get the user's bank account, ensuring they can only access their own
            account = get_object_or_404(BankAccount, account_number=account_number, user=request.user)

            # Check if account is suspended or blocked
            if account.suspended:
                return Response({"message": "Your account is suspended!"},
                                status=status.HTTP_400_BAD_REQUEST)
            if account.status == 'blocked':
                return Response({"message": "Your account is blocked!"},
                                status=status.HTTP_400_BAD_REQUEST)

            # Update the balance
            account.balance += amount
            account.save()

            return Response({"message": "Deposit successful", "new_balance": account.balance},
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from BankAccount.serializers import BankAccountDepositSerializer

# class DepositView(APIView):
#
#     def get(self, request):
#             accounts = BankAccount.objects.all()
#             serializer = BankAccountSerializer(accounts, many=True)
#             return Response(serializer.data)
#     def post(self, request):
#         print("Request data: ", request.data)
#
#         serializer = BankAccountDepositSerializer(data=request.data)
#         if serializer.is_valid():
#             account_number = serializer.validated_data['account_number']
#             amount = serializer.validated_data['amount']
#             print(f"Validated account number: {account_number}, amount: {amount}")
#             account = get_object_or_404(BankAccount, account_number=account_number)
#             print(f"Current balance: {account.balance}")
#             account.balance += amount
#             account.save()
#
#             print(f"New balance after deposit: {account.balance}")
#
#             return Response({"message": "Deposit successful", "new_balance": account.balance},
#                             status=status.HTTP_200_OK)
#         print("Validation errors: ", serializer.errors)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








#Last change 10:14

# class DepositView(APIView):
#
#     def get(self, request):
#         accounts = BankAccount.objects.all()
#         serializer = BankAccountSerializer(accounts, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         print("Request data: ", request.data)
#
#         serializer = BankAccountDepositSerializer(data=request.data)
#         if serializer.is_valid():
#             account_number = serializer.validated_data['account_number']
#             amount = serializer.validated_data['amount']
#             print(f"Validated account number: {account_number}, amount: {amount}")
#
#             account = get_object_or_404(BankAccount, account_number=account_number)
#
#             # Check if account is suspended or blocked
#             if account.suspended:
#                 return Response({"message": "Your account is suspended!."},
#                                 status=status.HTTP_400_BAD_REQUEST)
#             if account.status == 'blocked':
#                 return Response({"message": "Your account is blocked!."},
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#             print(f"Current balance: {account.balance}")
#             account.balance += amount
#             account.save()
#
#             print(f"New balance after deposit: {account.balance}")
#
#             return Response({"message": "Deposit successful", "new_balance": account.balance},
#                             status=status.HTTP_200_OK)
#
#         print("Validation errors: ", serializer.errors)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)









from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import BankAccount  # Assuming your BankAccount model is imported
from .serializers import BankAccountSerializer, BankAccountDepositSerializer  # Assuming these serializers are imported

# class DepositView(APIView):
#     def get(self, request):
#         # Check if the user is a superuser
#         if request.user.is_superuser:
#             # Superusers can see all accounts
#             accounts = BankAccount.objects.all()
#         else:
#             # Regular users can only see their own accounts
#             accounts = BankAccount.objects.filter(user=request.user)
#
#         serializer = BankAccountSerializer(accounts, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         print("Request data: ", request.data)
#
#         serializer = BankAccountDepositSerializer(data=request.data)
#         if serializer.is_valid():
#             account_number = serializer.validated_data['account_number']
#             amount = serializer.validated_data['amount']
#             print(f"Validated account number: {account_number}, amount: {amount}")
#
#             # Fetch the bank account, ensuring it's the user's account if not a superuser
#             if not request.user.is_superuser:
#                 account = get_object_or_404(BankAccount, account_number=account_number, user=request.user)
#             else:
#                 account = get_object_or_404(BankAccount, account_number=account_number)
#
#             # Check if account is suspended or blocked
#             if account.suspended:
#                 return Response({"message": "Your account is suspended!"},
#                                 status=status.HTTP_400_BAD_REQUEST)
#             if account.status == 'blocked':
#                 return Response({"message": "Your account is blocked!"},
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#             print(f"Current balance: {account.balance}")
#             account.balance += amount
#             account.save()
#
#             print(f"New balance after deposit: {account.balance}")
#
#             return Response({"message": "Deposit successful", "new_balance": account.balance},
#                             status=status.HTTP_200_OK)
#
#         print("Validation errors: ", serializer.errors)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





























#
# from BankAccount.models import BankAccount
# class WithdrawView(APIView):
#     def get(self, request):
#             accounts = BankAccount.objects.all()
#             serializer = BankAccountSerializer(accounts, many=True)
#             return Response(serializer.data)
#     def post(self, request):
#         serializer = BankAccountDepositSerializer(data=request.data)
#         if serializer.is_valid():
#             account_number = serializer.validated_data['account_number']
#             amount = serializer.validated_data['amount']
#             account = get_object_or_404(BankAccount, account_number=account_number)
#         if account.status == 'blocked':
#             return Response({"message": "Your account is blocked!"},status=status.HTTP_400_BAD_REQUEST)
#         if account.suspended:
#             print("Illegal operation: Account is suspended.")
#             return Response({"error": "Illegal operation: Account is suspended."}, status=status.HTTP_403_FORBIDDEN)
#
#         else:
#             if account.balance >= amount:
#                 account.balance -= amount
#                 account.save()
#                 return Response({"message": "Withdrawal successful", "new_balance": account.balance}, status=status.HTTP_200_OK)
#             else:
#                 return Response({"error": "Insufficient balance"},)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#






from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import BankAccount
from .serializers import BankAccountSerializer, BankAccountDepositSerializer  # Assume you have this serializer for withdraw

class WithdrawView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this view

    def get(self, request):
        # Check if the user is a superuser
        if request.user.is_superuser:
            # Superusers can see all accounts
            accounts = BankAccount.objects.all()
        else:
            # Regular users can only see their own accounts
            accounts = BankAccount.objects.filter(user=request.user)

        serializer = BankAccountSerializer(accounts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BankAccountDepositSerializer(data=request.data)  # Serializer for withdraw operation
        if serializer.is_valid():
            account_number = serializer.validated_data['account_number']
            amount = serializer.validated_data['amount']

            # Fetch the bank account, ensuring it's the user's account if not a superuser
            if request.user.is_superuser:
                account = get_object_or_404(BankAccount, account_number=account_number)
            else:
                account = get_object_or_404(BankAccount, account_number=account_number, user=request.user)

            # Check if account is suspended or blocked
            if account.status == 'blocked':
                return Response({"message": "Your account is blocked!"}, status=status.HTTP_400_BAD_REQUEST)
            if account.suspended:
                return Response({"error": "Illegal operation: Account is suspended."}, status=status.HTTP_403_FORBIDDEN)

            # Check if the balance is sufficient for withdrawal
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                return Response({"message": "Withdrawal successful", "new_balance": account.balance}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)























# class GetBalanceView(APIView):
#     def get(self, request):
#             accounts = BankAccount.objects.all()
#             serializer = BankAccountSerializer(accounts, many=True)
#             return Response(serializer.data)
#             return Response(serializer.data)
#     def post(self, request):
#             account_number = request.data.get('account_number')  # Get account number from request
#
#             if not account_number:
#                 return Response({"error": "Account number is required."}, status=status.HTTP_400_BAD_REQUEST)
#
#             # Retrieve the account using the account number
#             account = get_object_or_404(BankAccount, account_number=account_number)
#
#             # Return the balance of the account
#             return Response({"balance": account.balance}, status=status.HTTP_200_OK)










class GetBalanceView(APIView):
    def get(self, request):
        # Check if the user is a superuser
        if request.user.is_superuser:
            # Superusers can see all accounts and their balances
            accounts = BankAccount.objects.all()
        else:
            # Regular users can only see their own accounts
            accounts = BankAccount.objects.filter(user=request.user)

        serializer = BankAccountSerializer(accounts, many=True)
        return Response(serializer.data)

    def post(self, request):
        account_number = request.data.get('account_number')  # Get account number from request

        if not account_number:
            return Response({"error": "Account number is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the account using the account number, ensuring the user is authorized
        if request.user.is_superuser:
            # Superusers can retrieve any account
            account = get_object_or_404(BankAccount, account_number=account_number)
        else:
            # Regular users can only retrieve their own accounts
            account = get_object_or_404(BankAccount, account_number=account_number, user=request.user)

        # Return the balance of the account
        return Response({"Your balance is: ": account.balance}, status=status.HTTP_200_OK)

from decimal import Decimal  # Import Decimal

from decimal import Decimal  # Import Decimal







from decimal import Decimal

class TransferView(APIView):
    def get(self, request):
        # Check if the user is a superuser
        if request.user.is_superuser:
            # Superusers can see all accounts
            accounts = BankAccount.objects.all()
        else:
            # Regular users can only see their own accounts
            accounts = BankAccount.objects.filter(user=request.user)

        serializer = BankAccountSerializer(accounts, many=True)
        return Response(serializer.data)
    def post(self, request):
        source_account_number = request.data.get('source_account_number')
        target_account_number = request.data.get('target_account_number')
        amount = request.data.get('amount')

        # Validate amount
        try:
            amount = Decimal(amount)
            if amount <= 0:
                return Response({"error": "Transfer amount must be greater than zero."}, status=status.HTTP_400_BAD_REQUEST)
        except (ValueError, TypeError):
            return Response({"error": "Invalid transfer amount."}, status=status.HTTP_400_BAD_REQUEST)

        if not source_account_number or not target_account_number:
            return Response({"error": "Source and target account numbers are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve source and target accounts
        source_account = get_object_or_404(BankAccount, account_number=source_account_number)
        target_account = get_object_or_404(BankAccount, account_number=target_account_number)

        # Check if the user is superuser or owns the source account
        if not request.user.is_superuser and source_account.user != request.user:
            return Response({"error": "You can only transfer from your own account."}, status=status.HTTP_403_FORBIDDEN)

        # Check if the source account is blocked or suspended
        if source_account.suspended:
            return Response({"error": "Your account is suspended. Transfer is not allowed."}, status=status.HTTP_400_BAD_REQUEST)
        if source_account.status == 'blocked':
            return Response({"error": "Your Account is blocked. Transfer is not allowed."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the source account has sufficient balance
        if source_account.balance < amount:
            return Response({"error": "Insufficient balance in source account."}, status=status.HTTP_400_BAD_REQUEST)

        # Perform the transfer
        source_account.balance -= amount
        target_account.balance += amount
        source_account.save()
        target_account.save()

        return Response({
            "message": "Transfer successful",
            "source_new_balance": source_account.balance,
            "target_new_balance": target_account.balance
        }, status=status.HTTP_200_OK)
