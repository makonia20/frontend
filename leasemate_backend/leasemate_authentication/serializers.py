from rest_framework import serializers
from .models import LeasemateUser
from django.contrib.auth import authenticate

class SignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=30)  # New username field
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = LeasemateUser
        fields = ['username', 'phone', 'id_number', 'first_name', 'middle_name', 'last_name', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = LeasemateUser.objects.create_user(**validated_data)
        return user  # Return the created user instance

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()  # Changed from phone to username
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)  # Authenticate using username
        if not user:
            raise serializers.ValidationError("Invalid username or password")  # Update message
        data['user'] = user
        return data

    def to_representation(self, instance):
        return {
            'username': instance['user'].username,
            'message': 'Login successful'
        }

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeasemateUser
        fields = ['username', 'phone', 'id_number', 'first_name', 'middle_name', 'last_name']
