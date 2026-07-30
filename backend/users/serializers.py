from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import FarmerProfile, BuyerProfile, InspectorProfile


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


class FarmerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerProfile
        fields = ['id', 'user', 'farm_name', 'farm_location', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

    def validate(self, attrs):
        request = self.context.get("request")

        if not request:
            return attrs
        if request.user.role != "farmer":
            raise serializers.ValidationError(
                {"error": "Only users with the 'farmer' role can perform this action."}
            )
        has_profile = hasattr(request.user, "farmer_profile") 
        if self.instance is None and has_profile:
            raise serializers.ValidationError(
                {"error": "You already have a farmer profile."}
            )

        if self.instance is not None and not has_profile:
            raise serializers.ValidationError(
                {"error": "Profile does not exist to update."}
            )

        return attrs

    def create(self, validated_data):
        request = self.context["request"]

        return FarmerProfile.objects.create(
            user=request.user,
            **validated_data
        )


class BuyerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerProfile
        fields = ['id', 'user', 'company_name', 'company_location', 'created_at', 'updated_at', 'plan_tier']
        read_only_fields = ['plan_tier','user', 'created_at', 'updated_at']
    def validate(self, attrs):
        request =self.context.get("request")
        if request.user.role != "buyer":
            raise serializers.ValidationError(
                {"error": "Only users with the 'buyer' role can perform this action."}
            )
        has_profile = hasattr(request.user, "buyer_profile") 
        if self.instance is None and has_profile:
            raise serializers.ValidationError(
                {"error": "You already have a buyer profile."}
            )

        if self.instance is not None and not has_profile:
            raise serializers.ValidationError(
                {"error": "Profile does not exist to update."}
            )

        return attrs

    def create(self, validated_data):
        request = self.context["request"]

        return BuyerProfile.objects.create(
            user=request.user,
            **validated_data
        )
        
class InspectorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectorProfile
        fields = ['id', 'user', 'region', 'is_available', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']
    def validate(self, attrs):
        request =self.context.get("request")
        if request.user.role != "inspector":
            raise serializers.ValidationError(
                {"error": "Only users with the 'inspector' role can perform this action."}
            )
        has_profile = hasattr(request.user, "inspector_profile") 
        if self.instance is None and has_profile:
            raise serializers.ValidationError(
                {"error": "You already have a inspector profile."}
            )

        if self.instance is not None and not has_profile:
            raise serializers.ValidationError(
                {"error": "Profile does not exist to update."}
            )

        return attrs

    def create(self, validated_data):
        request = self.context["request"]

        return InspectorProfile.objects.create(
            user=request.user,
            **validated_data
        )
        
