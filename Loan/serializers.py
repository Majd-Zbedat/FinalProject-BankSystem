from rest_framework import serializers
from BankAccount.models import BankAccount

class GrantLoanSerializer(serializers.Serializer):
    account_number = serializers.CharField(max_length=20)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate_account_number(self, value):
        if not BankAccount.objects.filter(account_number=value).exists():
            raise serializers.ValidationError("The specified account does not exist.")
        return value

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("The loan amount must be greater than zero.")
        return value


# Loan/serializers.py
from rest_framework import serializers
from .models import Loan


# class LoanListSerializer(serializers.ModelSerializer):
#
#     # # Additional fields for calculations
#     # total_granted = serializers.SerializerMethodField()
#     # total_repaid = serializers.SerializerMethodField()
#     # remaining_balance = serializers.SerializerMethodField()
#     # # Loan/serializers.py
#     # from rest_framework import serializers
#
#
#     account_number = serializers.CharField(source='bank_account__account_number')
#     total_granted = serializers.DecimalField(max_digits=10, decimal_places=2)
#     total_repaid = serializers.DecimalField(max_digits=10, decimal_places=2)
#     remaining_balance = serializers.DecimalField(max_digits=10, decimal_places=2)
#     granted_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
#
#
#     class Meta:
#         model = Loan
#         fields = [
#             'account_number', 'amount', 'granted_at', 'repaid',
#             'total_granted', 'total_repaid', 'remaining_balance'
#         ]
#
#     def get_total_granted(self, obj):
#         # Total amount of the loan granted
#         return obj.amount
#
#     def get_total_repaid(self, obj):
#         # Total amount repaid towards this loan
#         return obj.amount_paid
#
#     def get_remaining_balance(self, obj):
#         # Calculate the remaining balance to be repaid
#         return obj.amount - obj.amount_paid

#
# from rest_framework import serializers
#
# class LoanListSerializer(serializers.Serializer):
#     account_number = serializers.CharField()
#     total_granted = serializers.DecimalField(max_digits=10, decimal_places=2)
#     total_repaid = serializers.DecimalField(max_digits=10, decimal_places=2)
#     remaining_balance = serializers.DecimalField(max_digits=10, decimal_places=2)


# # Loan/serializers.py
# from rest_framework import serializers
# from .models import Loan
#
# class SubLoanSerializer(serializers.Serializer):
#     id = serializers.IntegerField()  # Add loan ID field
#
#     amount = serializers.DecimalField(max_digits=10, decimal_places=2)
#     granted_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
#
# class LoanListSerializer(serializers.Serializer):
#     account_number = serializers.CharField()
#     email = serializers.EmailField()  # Include the user's email
#     total_granted = serializers.DecimalField(max_digits=10, decimal_places=2)
#
#     total_repaid = serializers.DecimalField(max_digits=10, decimal_places=2)
#     remaining_balance = serializers.DecimalField(max_digits=10, decimal_places=2)
#     sub_loans = SubLoanSerializer(many=True)
#
#
#
#






# Loan/serializers.py
from rest_framework import serializers
from .models import Loan

class SubLoanSerializer(serializers.Serializer):
    id = serializers.IntegerField()  # Include loan ID
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    granted_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    remaining_balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    is_repaid = serializers.BooleanField()  # Repayment status

class LoanListSerializer(serializers.Serializer):
    account_number = serializers.CharField()
    email = serializers.EmailField()  # Include the user's email

    total_loans = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_paid = serializers.DecimalField(max_digits=10, decimal_places=2)
    remaining_balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    sub_loans = SubLoanSerializer(many=True)





# Loan/serializers.py
from rest_framework import serializers
from .models import Loan

class RepayLoanSerializer(serializers.Serializer):
    account_number = serializers.CharField()  # Add account_number field

    loan_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

