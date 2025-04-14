from store_status.models import StoreStatus
from menu_hours.models import MenuHours
from timezones.models import Timezones
import os
from django.http import FileResponse
from datetime import timedelta,datetime
import pytz
import csv
from timezones.serializers import TimezonesSerializer
from menu_hours.serializers import MenuHoursSerializer
from collections import defaultdict
from report.models import Report
from django.shortcuts import get_object_or_404
from report.serializers import ReportSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from report.views import update_status_file
from concurrent.futures import ThreadPoolExecutor

def convert_local_to_utc(store_tz_str,local_dt):
    local_tz=pytz.timezone(store_tz_str or 'America/Chicago')
    return local_tz.localize(local_dt).astimezone(pytz.UTC)

# @api_view(['GET'])
# def report_all(request):
#     reports=Report.objects.all()
#     serializer=ReportSerializer(reports,many=True)
#     return Response(serializer.data)

@api_view(['GET'])
def report_details(request,report_id):
    print(report_id)
    obj=get_object_or_404(Report,report_id=report_id)
    if obj.status=='Running':
        return Response(obj.status)
    else:
        serializer=ReportSerializer(obj)
        return Response(serializer.data)
    
def dowload_report(request,report_id):
    obj=get_object_or_404(Report,report_id=report_id)
    if obj.status=='Running':
        return Response(obj.status)
    else:
        return FileResponse(obj.file.open('rb'),as_attachment=True,filename=f"{report_id}.csv")

def generate_report(report_id):
    print('Generating report...')
    
    os.makedirs('csv_reports',exist_ok=True)
    obj=get_object_or_404(Report,report_id=report_id)
    
    timezones=Timezones.objects.all()
    serializer=TimezonesSerializer(timezones,many=True)
    timezones=serializer.data
    
    current_timestamp='2024-10-14T23:55:18Z'
    current_timestamp_utc=datetime.strptime(current_timestamp,"%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.utc)
    
    last_hour_start=current_timestamp_utc-timedelta(hours=1)
    last_day=(current_timestamp_utc-timedelta(days=1)).date()
    last_week=[(current_timestamp_utc-timedelta(days=i)).date() for i in range(1,8)]
    
    rows=[]
    
    def process_report(item):
        store_id=item['store_id']
        
        print(item['id'])
        last_hour_intervals=get_store_working_hours(store_id,[last_hour_start.date()],item['timezone_str'] or 'America/Chicago')
        last_hour_intervals = last_hour_intervals.get(last_hour_start.date(),[])
        start_local,end_local=last_hour_intervals[0]
        uptime_last_hour,downtime_last_hour=calculate_uptime_downtime(StoreStatus.objects.filter(store_id=store_id,timestamp_utc__range=(max(start_local,last_hour_start),min(end_local,current_timestamp_utc))).order_by('timestamp_utc'),last_hour_start,current_timestamp_utc)
        uptime_last_hour=round(uptime_last_hour,2)
        downtime_last_hour=round(downtime_last_hour,2)
        
        last_day_intervals=get_store_working_hours(store_id,[last_day],item['timezone_str'] or 'America/Chicago')
        uptime_last_day=0
        downtime_last_day=0
        for (start,end) in last_day_intervals.get(last_day,[]):
            u,d=calculate_uptime_downtime(StoreStatus.objects.filter(store_id=store_id,timestamp_utc__range=(start,end)),start,end)
            uptime_last_day+=u
            downtime_last_day+=d
        uptime_last_day=round(uptime_last_day/60,2)
        downtime_last_day=round(downtime_last_day/60,2)
        
        last_week_intervals=get_store_working_hours(store_id,last_week,item['timezone_str'] or 'America/Chicago')
        uptime_last_week,downtime_last_week=0,0
        for day,intervals in last_week_intervals.items():
            for (start,end) in intervals:
                u,d=calculate_uptime_downtime(StoreStatus.objects.filter(store_id=store_id,timestamp_utc__range=(start,end)),start,end)
                uptime_last_week+=u
                downtime_last_week+=d
        uptime_last_week=round(uptime_last_week/60,2)
        downtime_last_week=round(downtime_last_week/60,2)
        
        return [store_id,uptime_last_hour,uptime_last_day,uptime_last_week,downtime_last_hour,downtime_last_day,downtime_last_week]
    
    with ThreadPoolExecutor() as executor:
        results=executor.map(process_report,timezones)
        rows=list(results)
        
    
    path=f"csv_reports/{report_id}.csv"
    with open(path,'w',newline='') as f:
        writer=csv.writer(f)
        writer.writerow(['store_id','uptime_last_hour','uptime_last_day','uptime_last_week','downtime_last_hour','downtime_last_day','downtime_last_week'])
        writer.writerows(rows)
        
    update_status_file(report_id,'Complete',path)
    print('Report generated successfully')
    
def get_store_working_hours(store_id,target_dates,tz_str):
    intervals=defaultdict(list)
    
    for date in target_dates:
        day=date.weekday()
        bhours=MenuHours.objects.filter(store_id=store_id,dayOfWeek=day)
        serializer=MenuHoursSerializer(bhours,many=True)

        if not bhours.exists():
            start_utc=convert_local_to_utc(tz_str,datetime.combine(date,datetime.min.time()))
            end_utc=convert_local_to_utc(tz_str,datetime.combine(date,datetime.max.time().replace(hour=23,minute=59)))
            intervals[date].append((start_utc,end_utc))
        else:
            for bh in bhours:
                start_local=datetime.combine(date,bh.start_time_local)
                end_local=datetime.combine(date,bh.end_time_local)
                start_utc=convert_local_to_utc(tz_str,start_local)
                end_utc=convert_local_to_utc(tz_str,end_local)
                intervals[date].append((start_utc,end_utc))
    
    return intervals

def calculate_uptime_downtime(store_status,start_utc,end_utc):
    total_uptime=timedelta()
    total_downtime=timedelta()

    # store_status=[r for r in store_status if r.timestamp_utc>=start_utc and r.timestamp_utc<=end_utc]
    store_status = list(store_status)
    store_status.sort(key=lambda x: x.timestamp_utc)

    if not store_status:
        return (0,(end_utc - start_utc).total_seconds() / 60)

    prev_timestamp=start_utc
    # prev=StoreStatus.objects.filter(store_id=store_status[0].store_id,timestamp_utc__lt=start_utc).order_by('-timestamp_utc').first()
    prev_status=store_status[0].status

    for record in store_status:
        current_timestamp=record.timestamp_utc
        if current_timestamp>end_utc:
            break

        duration=current_timestamp-prev_timestamp
        if duration.total_seconds()<0:
            duration=timedelta()

        if prev_status=='active':
            total_uptime+=duration
        else:
            total_downtime+=duration

        prev_timestamp=current_timestamp
        prev_status=record.status

    if prev_timestamp<end_utc:
        if prev_status=='active':
            total_uptime+=(end_utc-prev_timestamp)
        else:
            total_downtime+=(end_utc-prev_timestamp)

    return total_uptime.total_seconds()/60,total_downtime.total_seconds()/60