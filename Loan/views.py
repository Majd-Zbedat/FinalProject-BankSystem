from django.shortcuts import render

# Create your views here.


from rest_framework import generics
from .models import Loan
from .serializers import LoanSerializer
from rest_framework.permissions import IsAuthenticated

class LoanCreateView(generics.CreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

class LoanListView(generics.ListAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]
