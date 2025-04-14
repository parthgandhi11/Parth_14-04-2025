from  rest_framework import serializers
from .models import MenuHours

class MenuHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model=MenuHours
        fields=[
            'store_id',
            'dayOfWeek',
            'start_time_local',
            'end_time_local',
        ]