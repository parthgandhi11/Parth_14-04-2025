from django.urls import path
from . import views

urlpatterns=[
    path('<str:report_id>/',views.report_details),
    path('<str:report_id>/download',views.dowload_report),
]