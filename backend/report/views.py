from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
from .serializers import ReportSerializer
from .models import Report

# Create your views here.
def get_report(request):
    # Logic to generate the report
    report_data={
        'report_id': '12345',
        'status': 'Completed',
        'file': '/path/to/report/file.pdf'
    }
    
    return JsonResponse(report_data)

def create_report(data):
    serializer=ReportSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return serializer.data
    return JsonResponse(serializer.errors,status=400)

def update_status_file(report_id,status,file_path):
    try:
        report=Report.objects.get(report_id=report_id)
        report.status=status
        report.file=file_path
        report.save()
        return JsonResponse({'status': 'Report completed','report_id': report_id})
    except Report.DoesNotExist:
        return JsonResponse({'error': 'Report not found'},status=404)