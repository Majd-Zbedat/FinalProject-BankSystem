# # from django.db import models
# # from django.conf import settings
# # from BankAccount.models import BankAccount  # Import the BankAccount model
# #
# # class Loan(models.Model):
# #     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Reference to the user granting the loan
# #     bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)  # Reference to the user's bank account
# #     amount = models.DecimalField(max_digits=10, decimal_places=2)  # The total amount of the loan
# #     granted_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the loan is granted
# #     repaid = models.BooleanField(default=False)  # Indicates if the loan has been fully repaid
# #     amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Tracks repayments made on the loan
# #
# #     def __str__(self):
# #         return f"Loan for {self.user.email}: {self.amount} NIS"
# #
# #
# #
# from django.db import models
# from django.conf import settings
# from BankAccount.models import BankAccount
#
# class Loan(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Reference to the user granting the loan
#     bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)  # Reference to the user's bank account
#     amount = models.DecimalField(max_digits=10, decimal_places=2)  # The total amount of the loan
#     granted_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the loan is granted
#     repaid = models.BooleanField(default=False)  # Indicates if the loan has been fully repaid
#     amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Tracks repayments made on the loan
#
#     def __str__(self):
#         return f"Loan for {self.user.email}: {self.amount} NIS"

from django.db import models
from django.conf import settings
from BankAccount.models import BankAccount  # Import the BankAccount model

class Loan(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Reference to the user granting the loan
    bank_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)  # Reference to the user's bank account
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # The total amount of the loan
    granted_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the loan is granted
    repaid = models.BooleanField(default=False)  # Indicates if the loan has been fully repaid
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Tracks repayments made on the loan

    def __str__(self):
        return f"Loan for {self.user.email}: {self.amount} NIS"

    def repay(self, amount):
        """Repay the loan by the given amount."""
        if amount <= 0:
            raise ValueError("Repayment amount must be positive.")
        if self.amount_paid + amount >= self.amount:
            self.repaid = True
            self.amount_paid = self.amount  # Mark the loan as fully paid
        else:
            self.amount_paid += amount
        self.save()
