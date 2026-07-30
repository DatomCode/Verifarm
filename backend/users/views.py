from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import CustomUser
from .serializers import CustomUserSerializer
# Create your views here.

# Register User API View


class RegisterUserView(APIView):
    permission_classes = [AllowAny]  # Allow any user (authenticated or not) to access this view
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "User successfully registered!",
                "user": serializer.data,  # This returns username and email, but NOT password
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            }, status=201)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
