from  rest_framework import serializers
from .models import StoreStatus

class StoreStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model=StoreStatus
        fields=[
            'store_id',
            'status',
            'timestamp_utc',
        ]