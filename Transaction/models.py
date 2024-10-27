# # from django.db import models
# #
# # # Create your models here.
# # from django.db import models
# # from django.contrib.auth.models import User
# # from BankAccount.models import BankAccount
# # from django.contrib.auth import get_user_model
# # from User import models
# # from django.conf import settings
# #
# #
# #
# from django.db import models
# from django.conf import settings
# from BankAccount.models import BankAccount
#
# class Transaction(models.Model):
#     TRANSACTION_TYPES = [
#         ('deposit', 'Deposit'),
#         ('withdraw', 'Withdraw'),
#         ('transfer', 'Transfer'),
#     ]
#
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
#     fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
#     date = models.DateTimeField(auto_now_add=True)
#
#     def calculate_fee(self):
#         # Example fee logic: fee is 2% for transfers, 1% for withdrawals, 0% for deposits
#         if self.transaction_type == 'transfer':
#             return self.amount * 0.02
#         elif self.transaction_type == 'withdraw':
#             return self.amount * 0.01
#         return 0.0  # No fee for deposit
#
#     def save(self, *args, **kwargs):
#         # Automatically calculate fee before saving
#         self.fee = self.calculate_fee()
#         super().save(*args, **kwargs)
#
#     def _str_(self):
#         return f"{self.transaction_type} for {self.amount} NIS"
