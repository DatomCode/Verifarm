from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'phone_number', 'role', 'status']
        extra_kwargs = {
            'password': {'write_only': True},
        }


        def create(self, validated_data):
            user = get_user_model().objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                phone_number=validated_data.get('phone_number', ''),
                role=validated_data.get('role', ''),
                status=validated_data.get('status', '')
            )
            
            return user
        
