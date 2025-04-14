import csv
from datetime import datetime
from store_status.models import StoreStatus
from rest_framework import generics
import pytz
from rest_framework.response import Response
from .serializers import StoreStatusSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view

# Create your views here.
# def upload_data(request):
#     with open('C:/Users/Dell/Documents/loop_task/store_status.csv','r') as f:
#         reader=csv.DictReader(f)
#         StoreStatus.objects.all().delete()
#         cnt=0
#         for row in reader:
#             StoreStatus.objects.create(
#                 store_id=row['store_id'],
#                 timestamp_utc=datetime.strptime(row['timestamp_utc'].replace(' UTC',''),'%Y-%m-%d %H:%M:%S.%f').replace(tzinfo=pytz.UTC),
#                 status=row['status'].lower()
#             )
#             cnt+=1
#             print(cnt)
#     return Response({"message": "Data uploaded successfully."})

@api_view(['GET'])
def fetchAllStoreStatus(request):
    store_status=StoreStatus.objects.last()
    serializer=StoreStatusSerializer(store_status)
    return Response(serializer.data)
    # count=StoreStatus.objects.count()
    # return Response({'count': count})

# @api_view(['GET'])
def get_store_status_by_id_and_timestamp(request,store_id,start_time,end_time):
    try:
        store_status=StoreStatus.objects.filter(store_id=store_id,timestamp_utc__range=(start_time,end_time))
        serializer=StoreStatusSerializer(store_status,many=True)
        # .order_by('timestamp_utc')
        # print(store_status)
        return Response(serializer.data)
    except StoreStatus.DoesNotExist:
        return JsonResponse({'error': 'Store status not found'},status=404)