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

class BankAccountCreateView(generics.CreateAPIView):

    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated]

class BankAccountListView(generics.ListAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated]



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

class BankAccountSuspendUnsuspendView(APIView):
    def get(self, request):
        if request.user.is_superuser:
            accounts = BankAccount.objects.all()
        else:
            accounts = BankAccount.objects.filter(user=request.user)

        serializer = BankAccountSerializer(accounts, many=True)
        return Response(serializer.data)

    def put(self, request):
        # Check if the user is a superuser
        if not request.user.is_superuser:
            return Response({"error": "Only super users can suspend or unsuspend accounts."}, status=status.HTTP_403_FORBIDDEN)

        account_number = request.data.get('account_number')
        action = request.data.get('action')  # Expecting 'suspend' or 'unsuspend'

        if not account_number:
            return Response({"error": "Account number is required."}, status=status.HTTP_400_BAD_REQUEST)

        bank_account = get_object_or_404(BankAccount, account_number=account_number)

        if action == 'suspend':
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
class DepositView(APIView):
    def get(self, request):
        # List all bank accounts for selection
            accounts = BankAccount.objects.all()
            serializer = BankAccountSerializer(accounts, many=True)
            return Response(serializer.data)
    def post(self, request):
        serializer = BankAccountSerializer(data=request.data)
        if serializer.is_valid():
            account_number = serializer.validated_data['account_number']
            amount = serializer.validated_data['amount']
            account = get_object_or_404(BankAccount, account_number=account_number)

            account.balance += amount
            account.save()

            return Response({"message": "Deposit successful", "new_balance": account.balance},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#

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










class DepositView(APIView):

    def get(self, request):
        accounts = BankAccount.objects.all()
        serializer = BankAccountSerializer(accounts, many=True)
        return Response(serializer.data)

    def post(self, request):
        print("Request data: ", request.data)

        serializer = BankAccountDepositSerializer(data=request.data)
        if serializer.is_valid():
            account_number = serializer.validated_data['account_number']
            amount = serializer.validated_data['amount']
            print(f"Validated account number: {account_number}, amount: {amount}")

            account = get_object_or_404(BankAccount, account_number=account_number)

            # Check if account is suspended or blocked
            if account.suspended:
                return Response({"message": "Your account is suspended!."},
                                status=status.HTTP_400_BAD_REQUEST)
            if account.status == 'blocked':
                return Response({"message": "Your account is blocked!."},
                                status=status.HTTP_400_BAD_REQUEST)

            print(f"Current balance: {account.balance}")
            account.balance += amount
            account.save()

            print(f"New balance after deposit: {account.balance}")

            return Response({"message": "Deposit successful", "new_balance": account.balance},
                            status=status.HTTP_200_OK)

        print("Validation errors: ", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)











from BankAccount.models import BankAccount
class WithdrawView(APIView):
    def get(self, request):
            accounts = BankAccount.objects.all()
            serializer = BankAccountSerializer(accounts, many=True)
            return Response(serializer.data)
    def post(self, request):
        serializer = BankAccountDepositSerializer(data=request.data)
        if serializer.is_valid():
            account_number = serializer.validated_data['account_number']
            amount = serializer.validated_data['amount']
            account = get_object_or_404(BankAccount, account_number=account_number)
        if account.status == 'blocked':
            return Response({"message": "Your account is blocked!"},status=status.HTTP_400_BAD_REQUEST)
        if account.suspended:
            print("Illegal operation: Account is suspended.")
            return Response({"error": "Illegal operation: Account is suspended."}, status=status.HTTP_403_FORBIDDEN)

        else:
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                return Response({"message": "Withdrawal successful", "new_balance": account.balance}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Insufficient balance"},)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







class GetBalanceView(APIView):
    def get(self, request):
            accounts = BankAccount.objects.all()
            serializer = BankAccountSerializer(accounts, many=True)
            return Response(serializer.data)
            return Response(serializer.data)
    def post(self, request):
            account_number = request.data.get('account_number')  # Get account number from request

            if not account_number:
                return Response({"error": "Account number is required."}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve the account using the account number
            account = get_object_or_404(BankAccount, account_number=account_number)

            # Return the balance of the account
            return Response({"balance": account.balance}, status=status.HTTP_200_OK)