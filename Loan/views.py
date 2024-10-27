from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Loan
from .serializers import GrantLoanSerializer, LoanListSerializer
from BankAccount.models import BankAccount
from BankBalance.models import BankBalance


# Loan/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Loan
from .serializers import LoanListSerializer, SubLoanSerializer
from django.db.models import Sum, F

class LoanListView(generics.ListAPIView):
    serializer_class = LoanListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get all loans for superusers, or only user-specific loans for regular users
        loan_filter = Loan.objects.all() if self.request.user.is_superuser else Loan.objects.filter(user=self.request.user)

        # Group loans by account, including details for each loan (sub-loan)
        loans_by_account = (
            loan_filter
            .values('bank_account__account_number', 'user__email')  # Include user email
            .annotate(
                total_granted=Sum('amount'),
                total_repaid=Sum('amount_paid'),
                remaining_balance=Sum(F('amount') - F('amount_paid')),
                total_loans=Sum('amount'),  # Total amount of loans for each account
                total_paid=Sum('amount_paid'),  # Total paid for each account
            )
            .order_by('bank_account__account_number')
        )

        # Fetch each account's loans as sub-loans with timestamps and repayment status
        for loan_account in loans_by_account:
            account_number = loan_account['bank_account__account_number']
            loan_account['email'] = loan_account['user__email']  # Add user email
            loan_account['account_number'] = account_number

            # Fetch sub-loans for the account, including loan.id and repayment details
            sub_loans = Loan.objects.filter(bank_account__account_number=account_number).values(
                'id', 'amount', 'granted_at',
                'amount_paid',  # Amount paid so far
                'repaid'  # Whether the loan is fully repaid
            )

            # Add remaining balance and repayment status to each sub-loan
            for sub_loan in sub_loans:
                sub_loan['remaining_balance'] = sub_loan['amount'] - sub_loan['amount_paid']
                sub_loan['is_repaid'] = sub_loan['repaid']  # Add repayment status

            loan_account['sub_loans'] = list(sub_loans)  # Add the sub-loans for each account

        return loans_by_account



#
#
# # Loan/views.py
# from rest_framework import generics
# from rest_framework.permissions import IsAuthenticated
# from .models import Loan
# from .serializers import LoanListSerializer, SubLoanSerializer
# from django.db.models import Sum, F
#
# class LoanListView(generics.ListAPIView):
#     serializer_class = LoanListSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_queryset(self):
#         # Get all loans for superusers, or only user-specific loans for regular users
#         loan_filter = Loan.objects.all() if self.request.user.is_superuser else Loan.objects.filter(user=self.request.user)
#
#         # Group loans by account, including details for each loan (sub-loan)
#         loans_by_account = (
#             loan_filter
#             .values('bank_account__account_number', 'user__email')  # Include user email
#             .annotate(
#                 total_granted=Sum('amount'),
#                 total_repaid=Sum('amount_paid'),
#                 remaining_balance=Sum(F('amount') - F('amount_paid'))
#             )
#             .order_by('bank_account__account_number')
#         )
#
#         # Fetch each account's loans as sub-loans with timestamps
#         for loan_account in loans_by_account:
#             account_number = loan_account['bank_account__account_number']
#             loan_account['email'] = loan_account['user__email']  # Add user email
#             loan_account['account_number'] = account_number
#
#             # Fetch sub-loans for the account, including loan.id
#             sub_loans = Loan.objects.filter(bank_account__account_number=account_number).values('id', 'amount', 'granted_at')
#             loan_account['sub_loans'] = list(sub_loans)  # Add the sub-loans for each account
#
#         return loans_by_account















# Loan/views.py
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Loan
from .serializers import GrantLoanSerializer
from BankAccount.models import BankAccount
from BankBalance.models import BankBalance
from django.db.models import Sum

class GrantLoanView(generics.CreateAPIView):
    serializer_class = GrantLoanSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            account_number = serializer.validated_data['account_number']
            amount = serializer.validated_data['amount']

            # Check if the user is a superuser
            if request.user.is_superuser:
                # Superusers can grant loans to any account
                account = get_object_or_404(BankAccount, account_number=account_number)
            else:
                # Regular users can only grant loans for their own accounts
                account = get_object_or_404(BankAccount, account_number=account_number, user=request.user)

            # Check if the account is suspended or blocked
            if account.suspended:
                return Response({"error": "Your account is suspended."}, status=status.HTTP_400_BAD_REQUEST)
            if account.status == 'blocked':
                return Response({"error": "Your account is blocked."}, status=status.HTTP_400_BAD_REQUEST)

            # Retrieve the current bank balance
            bank_balance = get_object_or_404(BankBalance)

            # Check if the bank has enough balance to grant the loan
            if amount > bank_balance.total_balance:
                return Response({"error": "Insufficient bank balance to grant the loan."}, status=status.HTTP_400_BAD_REQUEST)

            # Calculate total loans granted to the user
            total_granted = Loan.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0

            # Check if the total loan limit is exceeded
            if total_granted + amount > 200000:
                return Response({"error": "Total loan amount cannot exceed 200,000 NIS."}, status=status.HTTP_400_BAD_REQUEST)

            # Create the loan
            loan = Loan.objects.create(user=request.user, bank_account=account, amount=amount)

            # Update the bank account balance and the bank's total balance
            account.balance += amount
            account.save()

            # Deduct the loan amount from the bank's total balance
            bank_balance.total_balance -= amount
            bank_balance.save()

            return Response({
                "message": "Loan granted successfully.",
                "account_number": account_number,
                "account_balance": account.balance,
                "borrowed_amount": amount,
                "bank_balance": bank_balance.total_balance,
                "loan_id": loan.id
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)













#
# # Loan/views.py
# from rest_framework import generics, status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from .models import Loan
# from .serializers import RepayLoanSerializer
# from BankBalance.models import BankBalance  # Import your BankBalance model
# from BankAccount.models import BankAccount  # Import your BankAccount model
#
# class RepayLoanView(generics.CreateAPIView):
#     serializer_class = RepayLoanSerializer
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             loan_id = serializer.validated_data['loan_id']
#             amount = serializer.validated_data['amount']
#             account_number = serializer.validated_data['account_number']
#
#             # Fetch the loan instance
#             loan = Loan.objects.filter(id=loan_id, user=request.user).first()
#             if not loan:
#                 return Response({"error": "Loan not found or you do not have permission to repay this loan."},
#                                 status=status.HTTP_404_NOT_FOUND)
#
#             # Check if the repayment amount is valid
#             if amount <= 0:
#                 return Response({"error": "Repayment amount must be positive."},
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#             # Check if the amount exceeds the remaining balance of the loan
#             remaining_balance = loan.amount - loan.amount_paid
#             if amount > remaining_balance:
#                 return Response({"error": "Repayment amount exceeds the remaining balance of the loan."},
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#             # Verify that the account number matches the user's bank account
#             account = BankAccount.objects.filter(account_number=account_number, user=request.user).first()
#             if not account:
#                 return Response({"error": "Account not found or you do not have permission to use this account."},
#                                 status=status.HTTP_404_NOT_FOUND)
#
#             # Fetch the current bank balance
#             bank_balance = BankBalance.objects.first()  # Assuming there's only one BankBalance instance
#             if amount > bank_balance.total_balance:
#                 return Response({"error": "Insufficient bank balance to make the repayment."},
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#             # Update loan repayment
#             loan.repay(amount)
#
#             # Update the bank balance
#             bank_balance.total_balance += amount  # Assuming repayments increase the bank balance
#             bank_balance.save()
#
#             # Prepare detailed feedback
#             feedback = {
#                 "message": "Loan repayment successful.",
#                 "loan_id": loan.id,
#                 "repayment_amount": amount,
#                 "new_remaining_balance": loan.amount - loan.amount_paid,
#                 "updated_bank_balance": bank_balance.total_balance,
#                 "total_paid": loan.amount_paid,
#                 "status": "Loan fully repaid" if loan.repaid else "Loan still outstanding"
#             }
#
#             return Response(feedback, status=status.HTTP_200_OK)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# Loan/views.py
# from rest_framework import generics, status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from .models import Loan
# from .serializers import RepayLoanSerializer
# from BankBalance.models import BankBalance  # Import your BankBalance model
# from BankAccount.models import BankAccount  # Import your BankAccount model
#
# class RepayLoanView(generics.CreateAPIView):
#     serializer_class = RepayLoanSerializer
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             loan_id = serializer.validated_data['loan_id']
#             amount = serializer.validated_data['amount']
#             account_number = serializer.validated_data['account_number']
#
#             # Check if the user is a superuser
#             if request.user.is_superuser:
#                 # Fetch the loan instance without user restriction
#                 loan = Loan.objects.filter(id=loan_id).first()
#                 if not loan:
#                     return Response({"error": "Loan not found."}, status=status.HTTP_404_NOT_FOUND)
#
#                 # Allow superuser to repay from any account number
#                 account = BankAccount.objects.filter(account_number=account_number).first()
#                 if not account:
#                     return Response({"error": "Account not found."}, status=status.HTTP_404_NOT_FOUND)
#             else:
#                 # Regular users can only repay their own loans
#                 loan = Loan.objects.filter(id=loan_id, user=request.user).first()
#                 if not loan:
#                     return Response({"error": "Loan not found or you do not have permission to repay this loan."}, status=status.HTTP_404_NOT_FOUND)
#
#                 # Verify that the account number matches the user's bank account
#                 account = BankAccount.objects.filter(account_number=account_number, user=request.user).first()
#                 if not account:
#                     return Response({"error": "Account not found or you do not have permission to use this account."}, status=status.HTTP_404_NOT_FOUND)
#
#             # Check if the repayment amount is valid
#             if amount <= 0:
#                 return Response({"error": "Repayment amount must be positive."}, status=status.HTTP_400_BAD_REQUEST)
#
#             # Check if the amount exceeds the remaining balance of the loan
#             remaining_balance = loan.amount - loan.amount_paid
#             if amount > remaining_balance:
#                 return Response({"error": "Repayment amount exceeds the remaining balance of the loan."}, status=status.HTTP_400_BAD_REQUEST)
#
#             # Fetch the current bank balance
#             bank_balance = BankBalance.objects.first()  # Assuming there's only one BankBalance instance
#             if amount > bank_balance.total_balance:
#                 return Response({"error": "Insufficient bank balance to make the repayment."}, status=status.HTTP_400_BAD_REQUEST)
#
#             # Update loan repayment
#             loan.repay(amount)
#
#             # Update the bank balance
#             bank_balance.total_balance += amount  # Assuming repayments increase the bank balance
#             bank_balance.save()
#
#             # Prepare detailed feedback
#             feedback = {
#                 "message": "Loan repayment successful.",
#                 "loan_id": loan.id,
#                 "repayment_amount": amount,
#                 "new_remaining_balance": loan.amount - loan.amount_paid,
#                 "updated_bank_balance": bank_balance.total_balance,
#                 "total_paid": loan.amount_paid,
#                 "status": "Loan fully repaid" if loan.repaid else "Loan still outstanding"
#             }
#
#             return Response(feedback, status=status.HTTP_200_OK)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#

























# # Loan/views.py
# from rest_framework import generics, status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from .models import Loan
# from .serializers import RepayLoanSerializer
# from BankBalance.models import BankBalance  # Import your BankBalance model
# from BankAccount.models import BankAccount  # Import your BankAccount model
#
# class RepayLoanView(generics.CreateAPIView):
#     serializer_class = RepayLoanSerializer
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             loan_id = serializer.validated_data['loan_id']
#             amount = serializer.validated_data['amount']
#             account_number = serializer.validated_data['account_number']
#
#             # Fetch the loan instance, ensuring it belongs to the user or the superuser
#             loan = Loan.objects.filter(id=loan_id).first()
#             if not loan:
#                 return Response({"error": "Loan not found."}, status=status.HTTP_404_NOT_FOUND)
#
#             # For regular users, check that the loan belongs to them
#             if not request.user.is_superuser and loan.user != request.user:
#                 return Response({"error": "You do not have permission to repay this loan."}, status=status.HTTP_403_FORBIDDEN)
#
#             # Ensure that the account number belongs to the loan's user for both regular and super users
#             account = BankAccount.objects.filter(account_number=account_number).first()
#             if not account or account.user != loan.user:
#                 return Response({"error": "Account not found or does not belong to the user associated with this loan."}, status=status.HTTP_404_NOT_FOUND)
#
#             # Check if the repayment amount is valid
#             if amount <= 0:
#                 return Response({"error": "Repayment amount must be positive."}, status=status.HTTP_400_BAD_REQUEST)
#
#             # Check if the amount exceeds the remaining balance of the loan
#             remaining_balance = loan.amount - loan.amount_paid
#             if amount > remaining_balance:
#                 return Response({"error": "Repayment amount exceeds the remaining balance of the loan."}, status=status.HTTP_400_BAD_REQUEST)
#
#             # Fetch the current bank balance
#             bank_balance = BankBalance.objects.first()  # Assuming there's only one BankBalance instance
#             if amount > bank_balance.total_balance:
#                 return Response({"error": "Insufficient bank balance to make the repayment."}, status=status.HTTP_400_BAD_REQUEST)
#
#             # Update loan repayment
#             loan.repay(amount)
#
#             # Update the bank balance
#             bank_balance.total_balance += amount  # Assuming repayments increase the bank balance
#             bank_balance.save()
#
#             # Prepare detailed feedback
#             feedback = {
#                 "message": "Loan repayment successful.",
#                 "loan_id": loan.id,
#                 "repayment_amount": amount,
#                 "new_remaining_balance": loan.amount - loan.amount_paid,
#                 "updated_bank_balance": bank_balance.total_balance,
#                 "total_paid": loan.amount_paid,
#                 "status": "Loan fully repaid" if loan.repaid else "Loan still outstanding"
#             }
#
#             return Response(feedback, status=status.HTTP_200_OK)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






#
#
#
# # Loan/views.py
# from rest_framework import generics, status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from .models import Loan
# from .serializers import RepayLoanSerializer
# from BankBalance.models import BankBalance  # Import your BankBalance model
# from BankAccount.models import BankAccount  # Import your BankAccount model
#
# class RepayLoanView(generics.CreateAPIView):
#     serializer_class = RepayLoanSerializer
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             loan_id = serializer.validated_data['loan_id']
#             amount = serializer.validated_data['amount']
#             account_number = serializer.validated_data['account_number']
#
#             # Fetch the loan instance
#             loan = Loan.objects.filter(id=loan_id).first()
#             if not loan:
#                 return Response({"error": "Loan not found."}, status=status.HTTP_404_NOT_FOUND)
#
#             # Ensure the account number matches the bank account associated with the loan
#             associated_account = loan.bank_account  # Get the associated bank account from the loan
#             if associated_account.account_number != account_number:
#                 return Response({"error": "Account number does not match the bank account associated with this loan."},
#                                 status=status.HTTP_404_NOT_FOUND)
#
#             # Check if the user is a superuser or if the loan belongs to the user
#             if not request.user.is_superuser and loan.user != request.user:
#                 return Response({"error": "You do not have permission to repay this loan."}, status=status.HTTP_403_FORBIDDEN)
#
#             # Check if the repayment amount is valid
#             if amount <= 0:
#                 return Response({"error": "Repayment amount must be positive."}, status=status.HTTP_400_BAD_REQUEST)
#
#             # Check if the amount exceeds the remaining balance of the loan
#             remaining_balance = loan.amount - loan.amount_paid
#             if amount > remaining_balance:
#                 return Response({"error": "Repayment amount exceeds the remaining balance of the loan."},
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#             # Fetch the current bank balance
#             bank_balance = BankBalance.objects.first()  # Assuming there's only one BankBalance instance
#             if amount > bank_balance.total_balance:
#                 return Response({"error": "Insufficient bank balance to make the repayment."},
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#             # Update loan repayment
#             loan.repay(amount)
#
#             # Update the bank balance
#             bank_balance.total_balance += amount  # Assuming repayments increase the bank balance
#             bank_balance.save()
#
#             # Prepare detailed feedback
#             feedback = {
#                 "message": "Loan repayment successful.",
#                 "loan_id": loan.id,
#                 "repayment_amount": amount,
#                 "new_remaining_balance": loan.amount - loan.amount_paid,
#                 "updated_bank_balance": bank_balance.total_balance,
#                 "total_paid": loan.amount_paid,
#                 "status": "Loan fully repaid" if loan.repaid else "Loan still outstanding"
#             }
#
#             return Response(feedback, status=status.HTTP_200_OK)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Loan/views.py
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Loan
from .serializers import RepayLoanSerializer
from BankBalance.models import BankBalance  # Import your BankBalance model
from BankAccount.models import BankAccount  # Import your BankAccount model
from django.shortcuts import get_object_or_404  # Import the shortcut

class RepayLoanView(generics.CreateAPIView):
    serializer_class = RepayLoanSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            loan_id = serializer.validated_data['loan_id']
            amount = serializer.validated_data['amount']
            account_number = serializer.validated_data['account_number']

            # Fetch the loan instance
            loan = get_object_or_404(Loan, id=loan_id)

            # Ensure the account number belongs to the loan's user for both regular users and superusers
            if request.user.is_superuser:
                # Superusers can use any account for repayment
                account = get_object_or_404(BankAccount, account_number=account_number)
            else:
                # Regular users can only use their own accounts
                account = get_object_or_404(BankAccount, account_number=account_number, user=request.user)

            # Check if the account is suspended or blocked
            if account.suspended:
                return Response({"error": "Your account is suspended."}, status=status.HTTP_400_BAD_REQUEST)
            if account.status == 'blocked':
                return Response({"error": "Your account is blocked."}, status=status.HTTP_400_BAD_REQUEST)

            # Ensure the loan belongs to the user or the superuser
            if not request.user.is_superuser and loan.user != request.user:
                return Response({"error": "You do not have permission to repay this loan."}, status=status.HTTP_403_FORBIDDEN)

            # Check if the repayment amount is valid
            if amount <= 0:
                return Response({"error": "Repayment amount must be positive."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the amount exceeds the remaining balance of the loan
            remaining_balance = loan.amount - loan.amount_paid
            if amount > remaining_balance:
                return Response({"error": "Repayment amount exceeds the remaining balance of the loan."}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch the current bank balance
            bank_balance = BankBalance.objects.first()  # Assuming there's only one BankBalance instance
            if amount > bank_balance.total_balance:
                return Response({"error": "Insufficient bank balance to make the repayment."}, status=status.HTTP_400_BAD_REQUEST)

            # Update loan repayment
            loan.repay(amount)

            # Update the bank balance
            bank_balance.total_balance += amount  # Assuming repayments increase the bank balance
            bank_balance.save()

            # Prepare detailed feedback
            feedback = {
                "message": "Loan repayment successful.",
                "loan_id": loan.id,
                "repayment_amount": amount,
                "new_remaining_balance": loan.amount - loan.amount_paid,
                "updated_bank_balance": bank_balance.total_balance,
                "total_paid": loan.amount_paid,
                "status": "Loan fully repaid" if loan.repaid else "Loan still outstanding"
            }

            return Response(feedback, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
