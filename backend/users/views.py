from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import FarmerProfile, BuyerProfile
from .serializers import CustomUserSerializer, FarmerProfileSerializer, BuyerProfileSerializer
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

class FarmerProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Allow only authenticated users to access this view

    # Helper method to get the farmer profile for the authenticated user
    def get_object(self):
        return self.request.user.farmer_profile  
    
    # create farmer profile
    def post(self, request):
        serializer = FarmerProfileSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()  
            return Response({
                "message": "Farmer profile successfully created!",
                "profile": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # get farmer profile
    def get(self, request):
        try:
            profile = self.get_object()
            serializer = FarmerProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except FarmerProfile.DoesNotExist:
            return Response({"error": "Farmer profile not found."}, status=status.HTTP_404_NOT_FOUND)
        
    # update farmer profile
    def patch(self, request):
        try:
            profile = self.get_object() # get the farmer profile for the authenticated user
            serializer = FarmerProfileSerializer(profile, data=request.data, context={"request": request}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Farmer profile successfully updated!",
                    "profile": serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except FarmerProfile.DoesNotExist:
            return Response({"error": "Farmer profile not found."}, status=status.HTTP_404_NOT_FOUND)
        
class BuyerProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Allow only authenticated users to access this view

    # Helper method to get the buyer profile for the authenticated user
    def get_object(self):
        return self.request.user.buyer_profile  
    
    # create buyer profile
    def post(self, request):
        serializer = BuyerProfileSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()  
            return Response({
                "message": "Buyer profile successfully created!",
                "profile": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # get buyer profile
    def get(self, request):
        try:
            profile = self.get_object()
            serializer = BuyerProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except BuyerProfile.DoesNotExist:
            return Response({"error": "Buyer profile not found."}, status=status.HTTP_404_NOT_FOUND)
        
    # update buyer profile
    def patch(self, request):
        try:
            profile = self.get_object() # get the buyer profile for the authenticated user
            serializer = BuyerProfileSerializer(profile, data=request.data, context={"request": request}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "message": "Buyer profile successfully updated!",
                    "profile": serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except BuyerProfile.DoesNotExist:
            return Response({"error": "Buyer profile not found."}, status=status.HTTP_404_NOT_FOUND)
