from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ProduceBatch
from .serializers import ProduceBatchSerializer
# Create your views here.

class ProduceBatchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Fetch all produce batches for the authenticated farmer.
        """
        farmer_profile = request.user.farmer_profile
        batches = ProduceBatch.objects.filter(farmer_profile=farmer_profile)
        serializer = ProduceBatchSerializer(batches, many=True)
        return Response(serializer.data, status=200)
