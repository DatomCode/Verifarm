from django.db import models
from django.contrib.auth.models import AbstractUser

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
