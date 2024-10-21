# from django.contrib.auth.models import User
# from rest_framework import serializers
# from rest_framework.authtoken.models import Token
# from django.contrib.auth import get_user_model
# from django.contrib.auth import authenticate
# from User import models
#
# User = get_user_model()
#
#
#
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
#         extra_kwargs = {'password': {'write_only': True}}
#
#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         return user
#
# class AuthTokenSerializer(serializers.Serializer):
#     """Serializer for user authentication and token generation"""
#     username = serializers.CharField()
#     password = serializers.CharField()
#
#     def validate(self, attrs):
#         """Check if the username and password are correct"""
#         username = attrs.get('username')
#         password = attrs.get('password')
#
#         user = authenticate(username=username, password=password)
#         if not user:
#             raise serializers.ValidationError("Invalid credentials")
#         attrs['user'] = user
#         return attrs
#
#     def create(self, validated_data):
#         """Create and return the token for the authenticated user"""
#         user = validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return token





#################################################################################


# from django.contrib.auth import get_user_model
# from rest_framework import serializers
# from rest_framework.authtoken.models import Token
# from django.contrib.auth import authenticate
#
# User = get_user_model()
#
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'first_name', 'last_name', 'email', 'password']
#         extra_kwargs = {'password': {'write_only': True}}
#
#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         return user
#
#
# class AuthTokenSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField()
#
#     def validate(self, attrs):
#         email = attrs.get('email')
#         password = attrs.get('password')
#
#         user = authenticate(username=email, password=password)  # Use email for authentication
#         if not user:
#             raise serializers.ValidationError("Invalid credentials")
#         attrs['user'] = user
#         return attrs
#
#     def create(self, validated_data):
#         user = validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return token



#################################################################3



from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     password = validated_data.get('password', None)
    #     if password:
    #         instance.set_password(password)
    #
    #     instance.save()
    #     return instance

    def update(self, instance, validated_data):
        """Update an existing user's details."""
        # Update the name if provided
        instance.name = validated_data.get('name', instance.name)

        # Update the password if provided and hash it
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])

        # Save the updated user instance
        instance.save()
        return instance



class UserDeleteSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(username=email, password=password)  # Use email for authentication
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        user = validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return token