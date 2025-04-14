import csv
from datetime import datetime
from menu_hours.models import MenuHours
from django.http import JsonResponse
from rest_framework.response import Response
from .models import MenuHours
from .serializers import MenuHoursSerializer
from rest_framework.decorators import api_view

# Create your views here.

# def upload_data(request):
#     with open('C:/Users/Dell/Documents/loop_task/menu_hours.csv','r') as f:
#         reader=csv.DictReader(f)
#         MenuHours.objects.all().delete()
#         cnt=0
#         for row in reader:
#             MenuHours.objects.create(
#                 store_id=row['store_id'],
#                 dayOfWeek=int(row['dayOfWeek']),
#                 start_time_local=datetime.strptime(row['start_time_local'],'%H:%M:%S').time(),
#                 end_time_local=datetime.strptime(row['end_time_local'],'%H:%M:%S').time()
#             )
#             cnt+=1
#             print(cnt)
#         return JsonResponse({"message": "Data uploaded successfully."})

@api_view(['GET'])
def fetchAllMenuHours(request):
    # menu_hours=MenuHours.objects.last()
    # serializer=MenuHoursSerializer(menu_hours)
    # return Response(serializer.data)
    count=MenuHours.objects.count()
    return Response({'count': count})

def get_menu_hours_by_id_and_day(request,store_id,day_of_week):
    try:
        menu_hours=MenuHours.objects.filter(store_id=store_id,dayOfWeek=day_of_week)
        serializer=MenuHoursSerializer(menu_hours,many=True)
        return Response(serializer.data)
    except MenuHours.DoesNotExist:
        return JsonResponse({'error': 'Menu hours not found'},status=404)