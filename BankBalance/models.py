from django.db import models

# Create your models here.
from django.db import models

class BankBalance(models.Model):
    total_balance = models.DecimalField(max_digits=12, decimal_places=2, default=10000000.00)  # Bank's balance starts with 10,000,000 NIS

    def __str__(self):
        return f"Bank Balance: {self.total_balance} NIS"
