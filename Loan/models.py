# from django.db import models
# from django.conf import settings
#
#
# # models.py
# from django.db import models
# from django.conf import settings
#
# from django.db import models
# from django.conf import settings
#
# from BankAccount.models import BankAccount
#
#
# class Loan(models.Model):
#     account_number = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=12, decimal_places=2)
#     status = models.CharField(max_length=10, default='pending')  # or 'approved', 'repaid', etc.
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"Loan for account {self.account_number} - Amount: {self.amount}"
















from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from BankAccount.models import BankAccount
from django.contrib.auth import get_user_model
from django.conf import settings




#
# class Loan(models.Model):
#     user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#
#     user = models.ForeignKey(user1, on_delete=models.CASCADE)
#     bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     granted_at = models.DateTimeField(auto_now_add=True)
#     repaid = models.BooleanField(default=False)
#
#     def __str__(self):
#         return f"Loan for {self.user.username}: {self.amount} NIS"



from django.db import models
from django.conf import settings
from BankAccount.models import BankAccount

class Loan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Correct ForeignKey reference
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    granted_at = models.DateTimeField(auto_now_add=True)
    repaid = models.BooleanField(default=False)

    def __str__(self):
        return f"Loan for {self.user.email}: {self.amount} NIS"  # Use user.email or any field you want to display
