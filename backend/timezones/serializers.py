from  rest_framework import serializers
from .models import Timezones

class TimezonesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Timezones
        fields=[
            'id',
            'store_id',
            'timezone_str',
        ]