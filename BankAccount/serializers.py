from rest_framework import serializers
from .models import BankAccount

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['user','name','account_number','balance','suspended','status']

    def get_status_color(self, obj):
        if obj.status == 'active':
            return 'green'
        elif obj.status == 'blocked':
            return 'black'
        elif obj.status == 'suspended':
            return 'red'  # If you want to display a different color for suspended accounts
        return 'gray'


#
# from rest_framework import serializers
# from .models import BankAccount
#
# class BankAccountSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BankAccount
#         fields = ['account_number', 'name', 'balance', 'suspended']
#


















# from rest_framework import serializers
# from .models import BankAccount
#
# class BankAccountSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(source='user.email', read_only=False)  # Access the email from the related User
#     name = serializers.CharField(source='user.name', read_only=True)     # Access the name from the related User
#
#     class Meta:
#         model = BankAccount
#         fields = ['account_number', 'email', 'name', 'balance']  # Include email and name from User
