from django.db import models
from django.contrib.auth.models import AbstractUser

from backend.verifarm import settings

# Create your models here.


class CustomUser(AbstractUser):
    # Add any additional fields you need for your custom user model

    ROLES = (
        ('admin', 'Platform Admin'),
        ('moderator', 'Compliance Moderator'),
        ('farmer', 'Farmer / Vendor'),
        ('buyer', 'Buyer / Business Owner'),
        ('inspector', 'Field Inspector'),
    )
    phone_number = models.CharField(
        max_length=15, blank=True, null=True)  # Example additional field
    role = models.CharField(max_length=50, blank=True,
                            null=True, choices=ROLES)
    status = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    pass

class FarmerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='farmer_profile')
    farm_name = models.CharField(max_length=255)
    farm_location = models.CharField(max_length=255, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Add any other fields specific to farmers

    def __str__(self):
        return self.farm_name

class BuyerProfile(models.Model):

    TIER_CHOICES = (
        ('free', 'Free'),
        ('pro', 'Pro'),
        ('enterprise', 'Enterprise'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='buyer_profile')
    company_name = models.CharField(max_length=255)
    company_location = models.CharField(max_length=255, db_index=True)
    plan_tier = models.CharField(max_length=50, choices=TIER_CHOICES, default='free')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Add any other fields specific to buyers

    def __str__(self):
        return f"{self.company_name}"