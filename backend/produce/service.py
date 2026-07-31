from decimal import Decimal
from typing import Optional
from django.db import transaction
from django.core.exceptions import ValidationError
from users.models import FarmerProfile
from .models import ProduceBatch


# State transition rules for your specific status values
ALLOWED_STATUS_TRANSITIONS = {
    'pending': ['verified', 'rejected'],
    'verified': [],  # End state
    'rejected': [],  # End state
}

# READ / QUERY SERVICES
def get_pending_inspection_queue(commodity_type: Optional[str] = None):
    """
    Fetches pending batches for inspectors.
    This query hits the partial index (idx_batch_pending_queue) on the DB.
    """
    queryset = ProduceBatch.objects.filter(status='pending')
    if commodity_type:
        queryset = queryset.filter(commodity_type__iexact=commodity_type)
    return queryset.order_by('created_at')

def get_farmer_batches(farmer_profile: FarmerProfile):
    """
    Fetches all produce batches owned by a given farmer.
    """
    return ProduceBatch.objects.filter(farmer_profile=farmer_profile)


# WRITE / MUTATION SERVICES
@transaction.atomic
def create_produce_batch(
    farmer_profile: FarmerProfile,
    commodity_type: str,
    quantity: Decimal,
    location: str
) -> ProduceBatch:
    """
    Creates a new batch using your model fields.
    """
    if quantity <= 0:
        raise ValidationError("Quantity must be greater than zero.")

    batch = ProduceBatch.objects.create(
        farmer_profile=farmer_profile,
        commodity_type=commodity_type.strip(),
        quantity=quantity,
        location=location.strip(),
        status='pending'  # Starts in pending
    )
    return batch


@transaction.atomic
def update_batch_status(
    batch_id: int,
    new_status: str
) -> ProduceBatch:
    """
    Validates and updates status according to state machine rules.
    """
    # Lock record during update to prevent race conditions
    batch = ProduceBatch.objects.select_for_update().get(id=batch_id)
    current_status = batch.status

    if current_status == new_status:
        return batch

    allowed_next_states = ALLOWED_STATUS_TRANSITIONS.get(current_status, [])
    if new_status not in allowed_next_states:
        raise ValidationError(
            f"Invalid status transition: Cannot change batch status from '{current_status}' to '{new_status}'."
        )

    batch.status = new_status
    batch.save(update_fields=['status', 'updated_at'])
    return batch


def verify_produce_batch(batch_id: int) -> ProduceBatch:
    """Shortcut function to set status to 'verified'."""
    return update_batch_status(batch_id=batch_id, new_status='verified')


def reject_produce_batch(batch_id: int) -> ProduceBatch:
    """Shortcut function to set status to 'rejected'."""
    return update_batch_status(batch_id=batch_id, new_status='rejected')