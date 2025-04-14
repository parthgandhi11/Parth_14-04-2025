import uuid
from rest_framework.response import Response
from rest_framework.decorators import api_view
from report.views import create_report
from get_report.views import generate_report
import threading
from report.models import Report

# Create your views here.
def run_report_async(report_id):
    generate_report(report_id)
    
@api_view(['GET'])
def trigger_report_view(request):
    # Report.objects.all().delete()
    report_id=str(uuid.uuid4())
    response=create_report({'report_id': report_id,'status': 'Running'})
    
    thread=threading.Thread(target=run_report_async,args=(report_id,))
    thread.start()
    
    return Response({'report_id':response['report_id']})

'''
report_id for complete status: 0d265c03-65ca-4345-adf2-22f54da57d1b
'''