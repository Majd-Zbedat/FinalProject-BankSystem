from django.db import models

from django.db import models

class BankBalance(models.Model):
    total_balance = models.DecimalField(max_digits=12, decimal_places=2, default=30000000.00)

    def __str__(self):
        return f"Bank Balance: {self.total_balance} NIS"
