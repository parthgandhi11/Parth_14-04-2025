from django.urls import path
from . import views

urlpatterns=[
    path('',views.trigger_report_view),
]