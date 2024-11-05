from django.shortcuts import render

# Create your views here.

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from .serializers import AuthTokenSerializer, UserDeleteSerializer
from rest_framework import generics, status
from django.shortcuts import render, redirect
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.views import View
from User.models import models
from rest_framework.views import APIView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from User.models import User


User = get_user_model()

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

class UserListView(generics.ListAPIView):
    def get(self, request):
        # Check if the user is a superuser
        if request.user.is_superuser:
            # Superusers can see all users
            users = User.objects.all()
        else:
            # Regular users can only see their own profile
            users = User.objects.filter(email=request.user.email)

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)  # Return the list of users
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class UserUpdateView(APIView):
    # def get(self, request):
    #     # List all users for selection
    #     users = User.objects.all()  # Get all users
    #     serializer = UserSerializer(users, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)  # Return the list of users

    def get(self, request):
        # Check if the user is a superuser
        if request.user.is_superuser:
            # Superusers can see all users
            users = User.objects.all()
        else:
            # Regular users can only see their own profile
            users = User.objects.filter(email=request.user.email)

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)  # Return the list of users


    def put(self, request):
        # Update user details based on the provided email
        email = request.data.get('email')  # Extract email from request data
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, email=email)  # Find the user by email
        serializer = UserSerializer(user, data=request.data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            serializer.save()  # Save the updated user details
            return Response(serializer.data, status=status.HTTP_200_OK)  # Return updated user data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return validation errors



# class UserDeleteView(APIView):
#     def delete(self, request):
#         # Use DELETE to delete a user based on email
#         serializer = UserDeleteSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             user = get_object_or_404(User, email=email)
#             user.delete()
#             return Response({"message": "User deleted successfully."}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteView(APIView):

    def get(self, request):
        # Check if the user is a superuser
        if request.user.is_superuser:
            # Superusers can see all users
            users = User.objects.all()
        else:
            # Regular users can only see their own profile
            users = User.objects.filter(email=request.user.email)

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)  # Return the list of users

    def post(self, request):
        # Use POST to delete a user based on email
        serializer = UserDeleteSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = get_object_or_404(User, email=email)
            user.delete()
            return Response({"message": "User deleted successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

<<<<<<< HEAD
=======


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)




















>>>>>>> 2b87986d (Last Version Of Project)
