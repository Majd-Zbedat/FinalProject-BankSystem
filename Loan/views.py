from rest_framework import generics, status
from rest_framework.response import Response
from .models import Loan
from .serializers import GrantLoanSerializer, LoanListSerializer
from BankAccount.models import BankAccount
from BankBalance.models import BankBalance
from .serializers import RepayLoanSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .serializers import LoanListSerializer, SubLoanSerializer
from django.db.models import Sum, F

class LoanListView(generics.ListAPIView):
    serializer_class = LoanListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        loan_filter = Loan.objects.all() if self.request.user.is_superuser else Loan.objects.filter(user=self.request.user)

        loans_by_account = (
            loan_filter
            .values('bank_account__account_number', 'user__email')
            .annotate(
                total_granted=Sum('amount'),
                total_repaid=Sum('amount_paid'),
                remaining_balance=Sum(F('amount') - F('amount_paid')),
                total_loans=Sum('amount'),
                total_paid=Sum('amount_paid'),
            )
            .order_by('bank_account__account_number')
        )

        for loan_account in loans_by_account:
            account_number = loan_account['bank_account__account_number']
            loan_account['email'] = loan_account['user__email']
            loan_account['account_number'] = account_number

            sub_loans = Loan.objects.filter(bank_account__account_number=account_number).values(
                'id', 'amount', 'granted_at',
                'amount_paid',
                'repaid'
            )

            for sub_loan in sub_loans:
                sub_loan['remaining_balance'] = sub_loan['amount'] - sub_loan['amount_paid']
                sub_loan['is_repaid'] = sub_loan['repaid']

            loan_account['sub_loans'] = list(sub_loans)

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




class GrantLoanView(generics.CreateAPIView):
    serializer_class = GrantLoanSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            account_number = serializer.validated_data['account_number']
            amount = serializer.validated_data['amount']

            if request.user.is_superuser:
                account = get_object_or_404(BankAccount, account_number=account_number)
            else:
                account = get_object_or_404(BankAccount, account_number=account_number, user=request.user)

            if account.suspended:
                return Response({"error": "Your account is suspended."}, status=status.HTTP_400_BAD_REQUEST)
            if account.status == 'blocked':
                return Response({"error": "Your account is blocked."}, status=status.HTTP_400_BAD_REQUEST)

            bank_balance = get_object_or_404(BankBalance)

            if amount > bank_balance.total_balance:
                return Response({"error": "Insufficient bank balance to grant the loan."}, status=status.HTTP_400_BAD_REQUEST)

            total_granted = Loan.objects.filter(user=request.user).aggregate(total=Sum('amount'))['total'] or 0

            if total_granted + amount > 200000:
                return Response({"error": "Total loan amount cannot exceed 200,000 NIS."}, status=status.HTTP_400_BAD_REQUEST)

            loan = Loan.objects.create(user=request.user, bank_account=account, amount=amount)

            account.balance += amount
            account.save()

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






<<<<<<< HEAD







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

=======
>>>>>>> 2b87986d (Last Version Of Project)
class RepayLoanView(generics.CreateAPIView):
    serializer_class = RepayLoanSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            loan_id = serializer.validated_data['loan_id']
            amount = serializer.validated_data['amount']
            account_number = serializer.validated_data['account_number']

            loan = get_object_or_404(Loan, id=loan_id)

            if request.user.is_superuser:
                account = get_object_or_404(BankAccount, account_number=account_number)
            else:
                account = get_object_or_404(BankAccount, account_number=account_number, user=request.user)

            if account.suspended:
                return Response({"error": "Your account is suspended."}, status=status.HTTP_400_BAD_REQUEST)
            if account.status == 'blocked':
                return Response({"error": "Your account is blocked."}, status=status.HTTP_400_BAD_REQUEST)

            if not request.user.is_superuser and loan.user != request.user:
                return Response({"error": "You do not have permission to repay this loan."}, status=status.HTTP_403_FORBIDDEN)

            if amount <= 0:
                return Response({"error": "Repayment amount must be positive."}, status=status.HTTP_400_BAD_REQUEST)

            remaining_balance = loan.amount - loan.amount_paid
            if amount > remaining_balance:
                return Response({"error": "Repayment amount exceeds the remaining balance of the loan."}, status=status.HTTP_400_BAD_REQUEST)

            bank_balance = BankBalance.objects.first()
            if amount > bank_balance.total_balance:
                return Response({"error": "Insufficient bank balance to make the repayment."}, status=status.HTTP_400_BAD_REQUEST)

            loan.repay(amount)

            bank_balance.total_balance += amount
            bank_balance.save()

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
