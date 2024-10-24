from rest_framework import serializers
from .models import BankAccount

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['user','name','account_number','balance','suspended','status']

    # class BankAccountSerializer(serializers.ModelSerializer):
    #     class Meta:
    #         model = BankAccount
    #         fields = ['account_number', 'balance', 'user', 'suspended', 'status']
    #         read_only_fields = ['balance', 'user', 'suspended', 'status']

    #############################################################
    def get_status_color(self, obj):
        if obj.status == 'active':
            return 'green'
        elif obj.status == 'blocked':
            return 'black'
        elif obj.status == 'suspended':
            return 'red'
        return 'gray'


############################################################




class BankAccountDepositSerializer(serializers.Serializer):
    account_number = serializers.CharField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    currency = serializers.CharField(max_length=3, default='USD', required=False)  # Optional if not using foreign currencies




class GetBalanceSerializer(serializers.Serializer):
    account_number = serializers.CharField(max_length=20)
