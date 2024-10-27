from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
from User import models



from django.db import models
from django.conf import settings




class BankAccount(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('blocked', 'Blocked'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Correctly reference the user model
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    name = models.CharField(max_length=255,default='Your Name')
    suspended = models.BooleanField(default=False) ####
    #closed = models.BooleanField(default=False)##
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')


    def __str__(self):
        return f"Account: {self.account_number} - {self.user.email}"  # Use email instead of username (or whatever you want to display)





# from django.db import models
# from django.conf import settings  # Use settings to reference the custom user model
#
# class BankAccount(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Correctly reference the user model
#     account_number = models.CharField(max_length=20, unique=True)
#     balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
#     name = models.CharField(max_length=255, default='Default Name')  # Add this line
#     suspended = models.BooleanField(default=False) ##
#
#     def __str__(self):
#         return f"Account: {self.account_number} - {self.user.email}"  # Use email instead of username (or whatever you want to display)
#








#
# from django.db import models
# from django.conf import settings  # Use settings to reference the custom user model
#
# class BankAccount(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Correctly reference the user model
#     account_number = models.CharField(max_length=20, unique=True)
#     balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
#
#     def __str__(self):
#         return f"Account: {self.account_number} - {self.user.email}"  # Use email instead of username (or whatever you want to display)
