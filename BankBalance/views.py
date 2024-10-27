from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import BankBalance

class BankBalanceView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]  # Require authentication

    def get_queryset(self):
        return BankBalance.objects.all()  # Retrieve all bank balances

    def get(self, request, *args, **kwargs):
        bank_balance = self.get_queryset().first()  # Get the first BankBalance object
        if bank_balance is None:
            return Response({"error": "Bank balance not found."}, status=404)

        return Response({
            "total_balance": str(bank_balance.total_balance)  # Return the total balance as a string
        })
