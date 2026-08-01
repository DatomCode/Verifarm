from rest_framework import serializers
from .models import ProduceBatch

class ProduceBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProduceBatch
        fields = ["commodity_type", "quantity", "location", "status", "created_at", "updated_at"]

    def create(self, validated_data):
        produce_batch = ProduceBatch.objects.create(
            farmer_profile=self.context["request"].user.farmer_profile,
            commodity_type=validated_data["commodity_type"],
            quantity=validated_data["quantity"],
            location=validated_data["location"],
            status=validated_data["status"]
        )
        return produce_batch
