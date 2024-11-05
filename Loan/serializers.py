from rest_framework import serializers
from BankAccount.models import BankAccount
from .models import Loan



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



class SubLoanSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    granted_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    remaining_balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    is_repaid = serializers.BooleanField()  # Repayment status

class LoanListSerializer(serializers.Serializer):
    account_number = serializers.CharField()
    email = serializers.EmailField()

    total_loans = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_paid = serializers.DecimalField(max_digits=10, decimal_places=2)
    remaining_balance = serializers.DecimalField(max_digits=10, decimal_places=2)
    sub_loans = SubLoanSerializer(many=True)






class RepayLoanSerializer(serializers.Serializer):
    account_number = serializers.CharField()

    loan_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

