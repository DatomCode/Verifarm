from rest_framework import serializers
from .models import ProduceBatch

class ProduceBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProduceBatch
        fields = ["commodity_type", "quantity", "status", "created_at", "updated_at"]

    #  def create(self, validate):
    #     produce_batch = ProduceBatch.objects.create(
            
    #     )


