import csv
from timezones.models import Timezones
from django.http import JsonResponse
from rest_framework.response import Response
from .models import Timezones
from .serializers import TimezonesSerializer
from rest_framework.decorators import api_view

# Create your views here.

# def upload_data(request):
#     with open('C:/Users/Dell/Documents/loop_task/timezones.csv','r') as f:
#         reader=csv.DictReader(f)
#         Timezones.objects.all().delete()
#         cnt=0
#         for row in reader:
#             Timezones.objects.create(
#                 store_id=row['store_id'],
#                 timezone_str=row['timezone_str']
#             )
#             cnt+=1
#             print(cnt)
#         return Response({"message": "Data uploaded successfully."})

@api_view(['GET'])
def fetchAllTimezones(request):
    # timezones=Timezones.objects.last()
    # serializer=TimezonesSerializer(timezones)
    # return Response(serializer.data)
    count=Timezones.objects.count()
    return Response({'count': count})