# from rest_framework import serializers
# from .models import Loan
#
# from rest_framework import serializers
# from .models import Loan
#
# # serializers.py
# from rest_framework import serializers
# from .models import Loan
#
# from rest_framework import serializers
# from .models import Loan
#
# class GrantLoanSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Loan
#         fields = ['account_number', 'amount']


from rest_framework import serializers
from .models import Loan

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['id', 'user', 'bank_account', 'amount', 'granted_at', 'repaid']
