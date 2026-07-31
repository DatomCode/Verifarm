from django.db import models
from apps.users.models import FarmerProfile  # Adjust path to your user app


class ProduceBatch(models.Model):
    # Standard choice tuple instead of set {} to avoid migration bugs
    STATUS_CHOICES = (
        ('pending', 'pending'),
        ('verified', 'verified'),
        ('rejected', 'rejected'),
    )

    # Django automatically names the DB column 'farmer_profile_id'
    farmer_profile = models.ForeignKey(
        FarmerProfile, 
        on_delete=models.PROTECT, 
        related_name='produce_batches'
    )
    commodity_type = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default='pending')
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'produce_batches'
        indexes = [
            # Composite Index (status, commodity_type, farmer_profile)
            models.Index(
                fields=['status', 'commodity_type', 'farmer_profile'],
                name='idx_batch_status_cmdty_farmer'
            ),
            # Partial Index targeting 'pending' batches for fast queue scanning
            models.Index(
                fields=['commodity_type', 'created_at'],
                condition=models.Q(status='pending'),
                name='idx_batch_pending_queue'
            ),
        ]

    def __str__(self):
        return f"{self.commodity_type} - {self.quantity} ({self.status})"