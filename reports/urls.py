from django.urls import path
from . import views

app_name = 'reports'
urlpatterns = [
    path('', views.report_list, name='list'),
    path('download/pdf/', views.generate_pdf_report, name='pdf'),
    path('download/csv/', views.generate_csv_report, name='csv'),
]
