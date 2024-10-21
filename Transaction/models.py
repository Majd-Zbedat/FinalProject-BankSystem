# from django.db import models
#
# # Create your models here.
# from django.db import models
# from django.contrib.auth.models import User
# from BankAccount.models import BankAccount
# from django.contrib.auth import get_user_model
# from User import models
# from django.conf import settings
#
#
#
#
# class Transaction(models.Model):
#     TRANSACTION_TYPES = [
#         ('deposit', 'Deposit'),
#         ('withdraw', 'Withdraw'),
#         ('transfer', 'Transfer'),
#     ]
#     user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#
#     user = models.ForeignKey(user1, on_delete=models.CASCADE)
#     bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
#     fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
#     date = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.transaction_type} for {self.amount} NIS"

from django.db import models
from django.conf import settings
from BankAccount.models import BankAccount


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
        ('transfer', 'Transfer'),
    ]

    # Correct ForeignKey reference to custom user model
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Correct ForeignKey reference

    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} for {self.amount} NIS"
